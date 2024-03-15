"""Defines URL patterns for quiz."""

from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Commitment page
    path('commitment/<int:quiz_id>/', views.commitment, name='commitment'),
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
    # Make quiz page
    path('make_quiz/', views.make_quiz, name='make_quiz'),
    # Show all quizzes for teacher
    path('quizzes/', views.quizzes, name='quizzes'),
    # Show a single quiz to quiz designer
    path('quiz_page/<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    # Quiz page
    path('take_quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    # my_panel for student
    path('my_panel/', views.my_panel, name='my_panel'),
    # page for quiz_answer result
    path('quiz_answer_result/<int:quiz_answer_id>/', views.quiz_answer_result, name='quiz_answer_result'),
]
