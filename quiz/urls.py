"""Defines URL patterns for quiz."""

from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Quiz page
    path('quiz/', views.quiz, name='quiz'),
    # Page for adding a new question
    path('add_question/', views.add_question, name='add_question'),
]
