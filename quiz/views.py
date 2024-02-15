from django.shortcuts import render
from django.forms import formset_factory

from .models import Question
from .forms import AnswerForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question_num = 2
    AnswerFormSet = formset_factory(AnswerForm, extra=question_num)
    question_texts = [''] * question_num
    for question_id in range(1, question_num + 1):
        question = Question.objects.get(id=question_id)
        question_texts[question_id - 1] = question.text

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

    context = {'question_texts': question_texts, 'formset': AnswerFormSet, 'evaluation': evaluation}
    return render(request, 'quiz/quiz.html', context)
