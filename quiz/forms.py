from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'user_answer']
        labels = {'text': 'question text', 'user_answer': 'write your answer...'}
