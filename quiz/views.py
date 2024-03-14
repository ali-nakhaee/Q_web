from datetime import datetime

from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from django.http import Http404, HttpResponse

from .models import Question, Quiz, QuestionAnswer, QuizAnswer
from .forms import QuestionForm, AddQuestionForm


def index(request):
    """The home page for Q_web."""
    print(request.user)
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
def take_quiz(request, quiz_id):
    user = request.user
    quiz = Quiz.objects.get(id=quiz_id)

    questions = []
    questions_values = quiz.questions.values()
    for question in questions_values:
        questions.append({'id': question['id'], 'text': question['text'],
                          'true_answer': question['true_answer']})
    if request.method == "GET":
        # check if the user has taken the quiz in the past
        if len(QuizAnswer.objects.filter(user=user, quiz=quiz)) != 1:
            return HttpResponse('You have taken this quiz in the past!')
        else:
            if QuizAnswer.objects.get(user=user, quiz=quiz).answer_duration != 1:
                return HttpResponse('You have taken this quiz in the past!')
            else:
                context = {'title': quiz.title, 'quiz_id': quiz.id,
                           'duration': quiz.duration, 'questions': questions}
                return render(request, 'quiz/take_quiz.html', context)
    
    elif request.method == "POST":
        quiz_answer = QuizAnswer.objects.filter(quiz=quiz, user=user).order_by('-date_started')[0]
        if quiz_answer.answer_duration != 1:
            return HttpResponse('You have taken this quiz in the past!')
        quiz_duration = quiz_answer.quiz.duration * 60
        submit_time = datetime.now().astimezone()
        if (submit_time - quiz_answer.date_started).total_seconds() > (quiz_duration + 10):
            return HttpResponse('Your answer is out of duration!')
        else:
            all_questions_num = len(questions)
            true_answers_num = 0
            for i in range(len(questions)):
                user_answer = request.POST.get(f"answer_{i}")
                question_id = questions[i]['id']
                question = Question.objects.get(id=question_id)
                if user_answer != '':
                    is_answered = True
                    if float(user_answer) == questions[i]['true_answer']:
                        evaluation = True
                        true_answers_num += 1
                    else:
                        evaluation = False
                else:
                    user_answer = None
                    is_answered = False
                    evaluation = False
                question_answer = QuestionAnswer.objects.create(question=question, user_answer=user_answer,
                                                                quiz=quiz, is_answered=is_answered,
                                                                evaluation=evaluation, quiz_answer=quiz_answer)

            percent = (true_answers_num / all_questions_num) * 100
            quiz_answer.percent = percent
            quiz_answer.date_answered = datetime.now().astimezone()
            answer_duration = (quiz_answer.date_answered - quiz_answer.date_started).total_seconds()
            quiz_answer.answer_duration = answer_duration
            quiz_answer.save()
            print('finish time:')
            print(quiz_answer.date_answered)
            print('duration:')
            print(answer_duration)
            return HttpResponse('quiz ended!')

    else:
        return HttpResponse('method not allowed!')


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
def commitment(request, quiz_id):
    # Commitment page before start the quiz.
    if request.method == "GET":
        return render(request, 'quiz/commitment.html', {'quiz_id': quiz_id})
    elif request.method == "POST":
        user = request.user
        quiz = Quiz.objects.get(id=quiz_id)
        quiz_answer = QuizAnswer.objects.create(user=user, quiz=quiz, answer_duration=1,
                                                percent=0)
        print('quiz started')
        return redirect("quiz:take_quiz", quiz_id=quiz_id)
    else:
        return HttpResponse("method not allowed")


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
        is_published = request.POST.get('is_published')
        print(is_published)
        if is_published:
            is_published = True
        else:
            is_published = False
        question_ids = []
        for i in range(len(questions)):
            is_in_quiz = request.POST.get(f"is_in_quiz_{i}")
            print(is_in_quiz)
            if is_in_quiz:
                question_ids.append(questions[i]['question_id'])
        print(question_ids, title)

        # make new object of Quiz model
        new_quiz = Quiz(title=title, designer=request.user, duration=duration,
                        is_published=is_published, answer_published=False)
        new_quiz.save()

        quiz_questions = Question.objects.filter(id__in=question_ids)
        for question in quiz_questions:
            new_quiz.questions.add(question)

        messages.success(request, 'کوییز با موفقیت ایجاد شد.')
        return redirect('quiz:quizzes')


@login_required
def quizzes(request):
    """ Show all quizzes for the teacher. """
    quizzes = Quiz.objects.filter(designer=request.user).order_by('-date_added')
    context = {'quizzes': quizzes}
    return render(request, 'quiz/quizzes.html', context)


@login_required
def quiz_page(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.designer != request.user:
        raise Http404
    if request.method != "POST":
        questions = quiz.questions.values('text', 'true_answer')
        context = {'title': quiz.title, 'questions': questions, 'duration': quiz.duration,
                   'is_published': quiz.is_published, 'answer_published': quiz.answer_published,
                   'quiz_id': quiz.id}
        return render(request, 'quiz/quiz_page.html', context)

    else:
        title = request.POST.get('quiz_title')
        duration = request.POST.get('duration')
        is_published = request.POST.get('is_published')
        if is_published:
            is_published = True
        else:
            is_published = False
        answer_published = request.POST.get('answer_published')
        if answer_published:
            answer_published = True
        else:
            answer_published = False
        quiz.title = title
        quiz.duration = duration
        quiz.is_published = is_published
        quiz.answer_published = answer_published
        quiz.save()
        messages.success(request, 'کوییز با موفقیت اصلاح شد.')
        return redirect('quiz:quizzes')


@login_required
def my_panel(request):
    user = request.user
    published_quizzes_ids = Quiz.objects.filter(is_published=True).values_list('id', flat=True)
    user_quizanswer_ids = QuizAnswer.objects.filter(user=user).values_list('quiz__id', flat=True)
    not_answered_quiz_ids = []
    for quiz_id in published_quizzes_ids:
        if quiz_id not in user_quizanswer_ids:
            not_answered_quiz_ids.append(quiz_id)
    print(published_quizzes_ids, user_quizanswer_ids, not_answered_quiz_ids)
    return HttpResponse('hi')
