from django.shortcuts import render, redirect
from django.forms import formset_factory

from .models import Question
from .forms import QuestionForm, AddQuestionForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


def quiz(request):
    """ Show quiz page. """
    question_num = Question.objects.all().count()
    questions = []
    for question_id in range(1, question_num + 1):
        question = Question.objects.get(id=question_id)
        questions.append({'text': question.text, 'true_answer': question.true_answer, 'user_answer': ''})

    QuestionFormSet = formset_factory(QuestionForm, extra=0)

    if request.method != 'POST':
        # No data submitted; create a blank Quiz.
        formset = QuestionFormSet(initial=questions)
        percent = 0
    else:
        # POST data submitted; process data.
        formset = QuestionFormSet(data=request.POST, initial=questions)
        query_dict = request.POST
        data = query_dict.copy()
        true_answers_num = 0
        if formset.is_valid():
            for i in range(0, question_num):
                if formset.cleaned_data[i]['user_answer']:
                    user_answer = formset.cleaned_data[i]['user_answer']
                    true_answer = Question.objects.get(id=i+1).true_answer
                    if float(user_answer) == true_answer:
                        data[f'form-{i}-evaluation'] = 'Your answer is True.'
                        true_answers_num += 1
                    else:
                        data[f'form-{i}-evaluation'] = 'Your answer is False.'
                else:
                    data[f'form-{i}-evaluation'] = "You didn't answer."
        formset = QuestionFormSet(data=data, initial=questions)
        percent = round((true_answers_num / question_num) * 100)
    context = {'formset': formset, 'percent': percent}
    return render(request, 'quiz/quiz.html', context)


def add_question(request):
    """ Add a new question to database. """
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = AddQuestionForm()
    else:
        # POST data submitted; process data.
        form = AddQuestionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'quiz/add_question.html', context)
