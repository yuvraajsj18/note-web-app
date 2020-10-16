from os import name
from django.urls import path

from . import views

app_name = "note"
urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),

    # api endpoints
    path('note', views.note, name="note"),
    path('note/edit', views.note_edit, name="note_edit"),
    path('note/edit/archive', views.note_archive, name="note_archive"),
    path('labels', views.labels, name="labels"),
]