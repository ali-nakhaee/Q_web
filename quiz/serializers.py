from rest_framework import serializers

from .models import Quiz, Question


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'duration']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'true_answer']   #'__all__'