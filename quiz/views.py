from django.shortcuts import render

from .models import Question
from .forms import AnswerForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question_texts = []
    for question_id in range(1, 3):
        question = Question.objects.get(id=question_id)
        question_texts.append(question.text)

    evaluation = []
    if request.method != 'POST':
        # No data submitted; create a blank Quiz.
        form = AnswerForm()
    
    else:
        # POST data submitted; process data.
        form = AnswerForm(data=request.POST)
        user_answer1 = request.POST.get('answer1')
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
            evaluation.append(f"Your answer is False. Correct answer is {question.answer}.")

    context = {'question_texts': question_texts, 'form': form, 'evaluation': evaluation}
    return render(request, 'quiz/quiz.html', context)
