from django.shortcuts import render
from django.forms import formset_factory

from .models import Question
from .forms import QuestionForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question_num = 3
    questions = []
    for question_id in range(1, question_num + 1):
        question = Question.objects.get(id=question_id)
        questions.append({'text': question.text, 'true_answer': question.true_answer, 'user_answer': ''})

    QuestionFormSet = formset_factory(QuestionForm, extra=0)

    if request.method != 'POST':
        # No data submitted; create a blank Quiz.
        formset = QuestionFormSet(initial=questions)
    else:
        # POST data submitted; process data.
        formset = QuestionFormSet(data=request.POST, initial=questions)
        query_dict = request.POST
        data = query_dict.copy()
        if formset.is_valid():
            for i in range(0, question_num):
                if formset.cleaned_data[i]['user_answer']:
                    user_answer = formset.cleaned_data[i]['user_answer']
                    true_answer = Question.objects.get(id=i+1).true_answer
                    if float(user_answer) == true_answer:
                        data[f'form-{i}-evaluation'] = 'Your answer is True.'
                    else:
                        data[f'form-{i}-evaluation'] = 'Your answer is False.'
                else:
                    data[f'form-{i}-evaluation'] = "You didn't answer."
        formset = QuestionFormSet(data=data, initial=questions)
    context = {'formset': formset}
    return render(request, 'quiz/quiz.html', context)
