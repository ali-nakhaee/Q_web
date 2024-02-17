from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': 'question text'}
        # widgets = {'text': forms.FloatField(attrs={'readonly': True})}

    evaluation = forms.BooleanField()
    user_answer = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(readonly=True)
