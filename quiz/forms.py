from django import forms

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': ''}


class AnswerForm(forms.Form):
    answer1 = forms.FloatField()
    answer2 = forms.FloatField()

