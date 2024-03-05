from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.http import Http404, HttpResponse

from .models import Question, Quiz
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
        # print(query_dict)
        data = query_dict.copy()
        true_answers_num = 0
        if formset.is_valid():
            for i in range(0, question_num):
                true_answer = questions[i]['true_answer']
                user_answer = formset.cleaned_data[i]['user_answer']
                if user_answer or user_answer == 0:
                    # The user has answered this question
                    if user_answer == true_answer:
                        data[f'form-{i}-evaluation'] = 'Your answer is True.'
                        true_answers_num += 1
                    else:
                        data[f'form-{i}-evaluation'] = ('Your answer is False. True answer'
                                                        f' is {true_answer}')
                else:
                    # The user has not answered this question
                    data[f'form-{i}-evaluation'] = f"You didn't answer. True answer is {true_answer}"

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


@login_required
def commitment(request):
    # Commitment page before start the quiz.
    return render(request, 'quiz/commitment.html')


@login_required
def make_quiz(request):
    user_questions = Question.objects.filter(owner=request.user).order_by('-date_added')
    questions = []
    for question in user_questions:
        questions.append({'text': question.text, 'true_answer': question.true_answer,
                          'is_in_quiz': False, 'question_id': question.id})

    if request.method != 'POST':
        context = {'questions': questions}
        return render(request, 'quiz/make_quiz.html', context)
    else:
        title = request.POST.get('quiz_title')
        duration = request.POST.get('duration')
        question_ids = []
        for i in range(len(questions)):
            is_in_quiz = request.POST.get(f"is_in_quiz_{i}")
            print(is_in_quiz)
            if is_in_quiz:
                question_ids.append(questions[i]['question_id'])
        print(question_ids, title)

        # make new object of Quiz model
        new_quiz = Quiz(title=title, designer=request.user, duration=duration)
        new_quiz.save()

        quiz_questions = Question.objects.filter(id__in=question_ids)
        for question in quiz_questions:
            new_quiz.questions.add(question)

        messages.success(request, 'The quiz has been added successfully.')
        return redirect('quiz:quizzes')


@login_required
def quizzes(request):
    """ Show all quizzes for the teacher. """
    quizzes = Quiz.objects.filter(designer=request.user).order_by('-date_added')
    context = {'quizzes': quizzes}
    return render(request, 'quiz/quizzes.html', context)


def quiz_page(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    title = quiz.title
    questions = quiz.questions.values('text', 'true_answer')
    duration = quiz.duration
    context = {'title': title, 'questions': questions, 'duration': duration}
    return render(request, 'quiz/quiz_page.html', context)