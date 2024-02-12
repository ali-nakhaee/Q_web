from django.shortcuts import render

from .models import Question
from .forms import AnswerForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question = Question.objects.get(id=1)

    if request.method != 'POST':
        # No data submitted; create a blank Quiz.
        form = AnswerForm()
        evaluation = ""
    else:
        # POST data submitted; process data.
        form = AnswerForm(data=request.POST)
        user_answer = request.POST.get('answer')
        if float(user_answer) == question.answer:
            evaluation = "Your answer is True."
        else:
            evaluation = f"Your answer is False. Correct answer is {question.answer}."

    context = {'question': question, 'form': form, 'evaluation': evaluation}
    return render(request, 'quiz/quiz.html', context)
