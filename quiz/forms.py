from django import forms

from .models import Question


class QuestionForm(forms.Form):

    text = forms.CharField()
    user_answer = forms.FloatField()
    evaluation = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(readonly=True)
        self.fields["user_answer"].required = False
        self.fields["evaluation"].required = False
