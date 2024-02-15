from django.shortcuts import render
from django.forms import formset_factory

from .models import Question
from .forms import QuestionForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question_num = 2
    QuestionFormSet = formset_factory(QuestionForm, extra=question_num)

    evaluation = []
    """if request.method != 'POST':
        # No data submitted; create a blank Quiz.

    
    else:
        # POST data submitted; process data.

        question = Question.objects.get(id=1)
        if float(user_answer1) == question.answer:
            evaluation.append("Your answer is True.")
        else:
            evaluation.append(f"Your answer is False. Correct answer is {question.answer}.")

        user_answer2 = request.POST.get('answer2')
        question = Question.objects.get(id=2)
        if float(user_answer2) == question.answer:
            evaluation.append("Your answer is True.")
        else:
            evaluation.append(f"Your answer is False. Correct answer is {question.answer}.")"""

    context = {'formset': QuestionFormSet, 'evaluation': evaluation}
    return render(request, 'quiz/quiz.html', context)
