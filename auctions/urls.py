from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("record", views.record, name="record"),
    path("workout/<date>", views.workout, name="workout"),
    path("jukebox/<workout>/<session_id>", views.jukebox, name="jukebox")
]
