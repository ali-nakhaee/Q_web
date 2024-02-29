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


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'true_answer']
        labels = {'text': 'text', 'true_answer': 'true answer'}


"""class QuizForm(forms.Form):
    question_text = forms.CharField()
    is_in_quiz = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question_text"].widget.attrs.update(readonly=True)"""
