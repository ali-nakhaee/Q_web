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
            for i in range(1, question_num):
                user_answer = formset.cleaned_data[i]['user_answer']
                true_answer = Question.objects.get(id=i-1).true_answer
                if float(user_answer) == true_answer:
                    data['form-0-evaluation'] = 'Your answer is True.'
                else:
                    data['form-0-evaluation'] = 'Your answer is False.'

            """a = formset.cleaned_data[0]['user_answer']
            data["form-0-evaluation"] = a
            answer1 = Question.objects.get(id=1).true_answer
            if float(a) == answer1:
                data['form-0-evaluation'] = 'Your answer is True.'
        else:
            data['form-0-evaluation'] = 'Your answer is False.'
        # data['form-0-user_answer'] """

        """for i in range(1, question_num + 1):
            answer = Question.objects.get(id=i).true_answer
            if float(data[i]['user_answer']) == answer:
                data[i]['user_answer'] = 'Your answer is True.'
            else:
                data[i]['user_answer'] = 'Your answer is False.' """

        formset = QuestionFormSet(data=data, initial=questions)

    context = {'formset': formset}
    return render(request, 'quiz/quiz.html', context)
