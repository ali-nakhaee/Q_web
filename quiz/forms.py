from django import forms

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': ''}


class AnswerForm(forms.ModelForm):
    # answer = forms.FloatField(initial=2.4)
    class Meta:
        model = Answer
        fields = ['answer']
