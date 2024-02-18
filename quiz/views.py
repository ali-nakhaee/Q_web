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

    evaluation = [''] * question_num
    if request.method != 'POST':
        # No data submitted; create a blank Quiz.
        formset = QuestionFormSet(initial=questions)
        evaluation[0] = 'hello'
        evaluation[1] = 'bye'
    else:
        # POST data submitted; process data.
        # request.data._mutable = True
        data = request.POST
        text1 = data['form-0-user_answer']
        evaluation.append(text1)
        formset = QuestionFormSet(data=data, initial=questions)
        answer1 = Question.objects.get(id=1).true_answer
        '''if float(data['form-0-user_answer']) == answer1:
            data['form-0-evaluation'] = 'Your answer is True.'
        else:
            data['form-0-evaluation'] = 'Your answer is False'  '''

        formset = QuestionFormSet(data=data, initial=questions)

    context = {'formset': formset, 'evaluation': evaluation}
    return render(request, 'quiz/quiz.html', context)
