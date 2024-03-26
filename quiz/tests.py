from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Question, Quiz, QuestionAnswer, QuizAnswer

User = get_user_model()


class TestQuestionModel(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='ali', password='123', first_name='ali',
                                   last_name='na')
        question1 = Question.objects.create(text='2+2=', owner=user1, true_answer=4)
        quiz1 = Quiz.objects.create(title='quiz1', designer=user1, duration=1,
                                    is_published=True, answer_published=True)
        quiz1.questions.add(question1)
        quiz_answer1 = QuizAnswer.objects.create(user=user1, quiz=quiz1, percent=100,
                                                 answer_duration=20)
        QuestionAnswer.objects.create(question=question1, quiz=quiz1, quiz_answer=quiz_answer1,
                                        user_answer=4, is_answered=True, evaluation=True)
        
        
    def test_question_answer(self):
        question_answer = QuestionAnswer.objects.get(question__text='2+2=')
        self.assertEqual(question_answer.user_answer, 4)

    def test_question_edit(self):
        pass

