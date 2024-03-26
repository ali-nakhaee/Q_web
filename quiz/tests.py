from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Question

User = get_user_model()


class TestQuestionModel(TestCase):
    def setUp(self):
        user = User.objects.create(username='ali', password='123', first_name='ali',
                                   last_name='na')
        Question.objects.create(text='2+2=', owner=user, true_answer=4)

    def test_question_answer(self):
        question = Question.objects.get(text='2+2=')
        self.assertEqual(question.true_answer, 4)
