"""Defines URL patterns for quiz."""

from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Quiz page
    path('quiz/', views.quiz, name='quiz'),
    # Page for show all questions
    path('questions/', views.questions, name='questions'),
    # Page for adding a new question
    path('add_question/', views.add_question, name='add_question'),
    # Page for editing a single question
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    # Page for confirm delete a single questions
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
]
