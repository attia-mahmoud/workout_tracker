from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Session(models.Model):
    user = models.CharField(max_length=64)
    date = models.DateField()
    workout = models.CharField(max_length=64)

class Weights(models.Model):
    session_number = models.IntegerField()
    exercise = models.CharField(max_length=64)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()

class Calisthenics(models.Model):
    session_number = models.IntegerField()
    exercise = models.CharField(max_length=64)
    sets = models.IntegerField()
    reps = models.IntegerField()

class Cardio(models.Model):
    session_number = models.IntegerField()
    exercise = models.CharField(max_length=64)
    distance = models.IntegerField()
    duration = models.IntegerField()


