from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text', 'user_answer']
        labels = {'text': 'question text', 'user_answer': 'write your answer...'}
        # widgets = {'text': forms.FloatField(attrs={'readonly': True})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(readonly=True)