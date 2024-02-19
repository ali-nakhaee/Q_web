from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['text']
        labels = {'text': 'question text'}
        # widgets = {'text': forms.FloatField(attrs={'readonly': True})}

    user_answer = forms.FloatField()
    evaluation = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(readonly=True)
        self.fields["user_answer"].required = False
        self.fields["evaluation"].required = False

