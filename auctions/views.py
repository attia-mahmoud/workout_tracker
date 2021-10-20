from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import datetime
import json
from django.forms.models import model_to_dict
from django.core import serializers

from .models import User, Session, Weights, Calisthenics, Cardio


def index(request):
    current_user = request.user
    recent_set = Session.objects.filter(user = current_user.username).latest('id')
    session = recent_set.id
    workout = recent_set.workout
    if workout == "weight":
        exercise_set = Weights.objects.get(session_number = session)
        exercise = exercise_set.exercise
        sets = exercise_set.sets
        reps = exercise_set.reps
        weight = exercise_set.weight
        return render(request, "auctions/index.html", {
        "exercise":exercise,
        "sets":sets,
        "reps":reps,
        "weight":weight,
        "workout":workout
        })
    elif workout == "calisthenics":
        exercise_set = Calisthenics.objects.get(session_number = session)  
        exercise = exercise_set.exercise
        sets = exercise_set.sets
        reps = exercise_set.reps
        return render(request, "auctions/index.html", {
        "exercise":exercise,
        "sets":sets,
        "reps":reps,
        "workout":workout
        })
    elif workout == "cardio":
        exercise_set = Cardio.objects.get(session_number = session)
        exercise = exercise_set.exercise
        duration = exercise_set.duration
        distance = exercise_set.distance
        return render(request, "auctions/index.html", {
        "exercise":exercise,
        "duration":duration,
        "distance":distance,
        "workout":workout
        })
        


    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add(request):
    if request.method == "GET":
        date = datetime.date.today()
        return render(request, "auctions/add.html", {
            "date": date
        })
    else:
        workout = request.POST.get("type")
        username = request.POST.get("username")
        date = datetime.date.today()
        current_user = request.user
        if workout == "weight":
            session = Session(user=username, date = date, workout = workout)
            session.save()
            session_id = session.id
            name = request.POST.get("exercise")
            sets = request.POST.get("sets")
            reps = request.POST.get("reps")
            weight = request.POST.get("weight")
            exercise = Weights(session_number = session_id, exercise = name, sets = sets, reps = reps, weight = weight)
            exercise.save()
            
        elif workout == "calisthenics":
            session = Session(user=current_user.username, date = date, workout = workout)
            session.save()
            session_id = session.id
            name = request.POST.get("exercise")
            sets = request.POST.get("sets")
            reps = request.POST.get("reps")
            exercise = Calisthenics(session_number = session_id, exercise = name, sets = sets, reps = reps)
            exercise.save()
            
        elif workout == "cardio":
            session = Session(user=current_user.username, date = date, workout = workout)
            session.save()
            session_id = session.id
            name = request.POST.get("exercise")
            distance = request.POST.get("distance")
            duration = request.POST.get("duration")
            exercise = Cardio(session_number = session_id, exercise = name, distance = distance, duration = duration)
            exercise.save()
            
        return HttpResponseRedirect(reverse("record"))

        

def record(request):
    current_user = request.user
    sessions = Session.objects.filter(user = current_user.username)
    unique_list = []
    approved_sessions = []
    for i in range(len(sessions)):
        if sessions[i].date not in unique_list:
            unique_list.append(sessions[i].date)
            approved_sessions.append(sessions[i])

    return render(request, "auctions/record.html", {
        "sessions": approved_sessions,
        "unique": unique_list

    })

def workout(request, date):
    current_user = request.user
    #olddate = request.POST.get("dates")
    date = datetime.datetime.strptime(date, '%b. %d, %Y')
    date = date.strftime('%Y-%m-%d')
    sessions = Session.objects.filter(user = current_user.username, date = date)
    
    sessions_json = serializers.serialize('json', sessions)
    sessions_json = json.dumps(sessions_json)
    
    #return render(request, "auctions/workout.html", {
        #"date": sessions_json
    #})
    
    return HttpResponse(sessions_json)

def jukebox(request, workout, session_id):
    if workout == "weight":
        exercise = Weights.objects.filter(session_number = session_id)
    elif workout == "calisthenics":
        exercise = Calisthenics.objects.filter(session_number = session_id)
    elif workout == "cardio":
        exercise = Cardio.objects.filter(session_number = session_id)
    exercise_json = serializers.serialize('json', exercise)
    exercise_json = json.dumps(exercise_json)
    return HttpResponse(exercise_json)

