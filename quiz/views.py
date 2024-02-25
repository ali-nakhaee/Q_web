from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.http import Http404

from .models import Question
from .forms import QuestionForm, AddQuestionForm


def index(request):
    """The home page for Q_web."""
    return render(request, 'quiz/index.html')


@login_required
def quiz(request):
    """ Show quiz page. """
    question_num = Question.objects.all().count()
    questions = []

    if question_num > 0:
        last_question_id = Question.objects.latest('id').id
    else:
        last_question_id = 0

    for question_id in range(1, last_question_id + 1):
        if Question.objects.filter(id=question_id).exists():
            question = Question.objects.get(id=question_id)
            questions.append({'text': question.text, 'true_answer': question.true_answer,
                              'user_answer': '', 'id': question.id})

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
                    true_answer = questions[i]['true_answer']
                    if float(user_answer) == true_answer:
                        data[f'form-{i}-evaluation'] = 'Your answer is True.'
                        true_answers_num += 1
                    else:
                        data[f'form-{i}-evaluation'] = 'Your answer is False.'
                else:
                    data[f'form-{i}-evaluation'] = "You didn't answer."

        formset = QuestionFormSet(data=data, initial=questions)
        if question_num > 0:
            percent = round((true_answers_num / question_num) * 100)
        else:
            percent = 0

    context = {'formset': formset, 'percent': percent}
    return render(request, 'quiz/quiz.html', context)


@login_required
@permission_required('quiz.add_question', raise_exception=True)
def add_question(request):
    """ Add a new question to database. """
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = AddQuestionForm()
    else:
        # POST data submitted; process data.
        form = AddQuestionForm(data=request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.owner = request.user
            new_question.save()
            messages.success(request, 'The question has been added successfully.')
            return redirect('quiz:questions')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'quiz/add_question.html', context)


@login_required
@permission_required('quiz.view_question', raise_exception=True)
def questions(request):
    """ Show all questions from database. """
    questions = Question.objects.filter(owner=request.user).order_by('-date_added')
    context = {'questions': questions}
    return render(request, 'quiz/questions.html', context)


@login_required
@permission_required('quiz.change_question', raise_exception=True)
def edit_question(request, question_id):
    """ Edit a single question. """
    question = Question.objects.get(id=question_id)
    # Make sure the topic belongs to the current user.
    if question.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current question.
        form = AddQuestionForm(instance=question)
    else:
        # POST data submitted; process data.
        form = AddQuestionForm(instance=question, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The question has been edited successfully.')
            return redirect('quiz:questions')

    context = {'form': form, 'question': question}
    return render(request, 'quiz/edit_question.html', context)


@login_required
@permission_required('quiz.delete_question', raise_exception=True)
def delete_question(request, question_id):
    """ Delete one question. """
    question = Question.objects.get(id=question_id)
    # Make sure the topic belongs to the current user.
    if question.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current question.
        context = {'question': question}
        return render(request, 'quiz/delete_question.html', context)
    else:
        # POST data submitted; process data.
        question.delete()
        messages.success(request, 'The question has been deleted successfully.')
        return redirect('quiz:questions')
