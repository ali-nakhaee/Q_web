from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Question, Quiz, QuestionAnswer, QuizAnswer

User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='ali', password='123', first_name='ali',
                                   last_name='na')
        question1 = Question.objects.create(text='2+2=', owner=user1, true_answer=4)
        quiz1 = Quiz.objects.create(title='quiz1', designer=user1, duration=1,
                                    is_published=True, answer_published=False)
        quiz1.questions.add(question1)
        quiz_answer1 = QuizAnswer.objects.create(user=user1, quiz=quiz1, percent=100,
                                                 answer_duration=20)
        QuestionAnswer.objects.create(question=question1, quiz=quiz1, quiz_answer=quiz_answer1,
                                        user_answer=4, is_answered=True, evaluation=True)
        
    def test_question(self):
        question = Question.objects.get(text='2+2=')
        self.assertEqual(question.owner.username, 'ali')
        
    def test_quiz(self):
        quiz = Quiz.objects.get(title='quiz1')
        self.assertTrue(quiz.is_published)
        self.assertFalse(quiz.answer_published)

    def test_quiz_answer(self):
        quiz_answer = QuizAnswer.objects.get(user__username='ali')
        self.assertEqual(quiz_answer.answer_duration, 20)
        
    def test_question_answer(self):
        question_answer = QuestionAnswer.objects.get(question__text='2+2=')
        self.assertEqual(question_answer.user_answer, 4)

class TestEditQuestionView(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='ali', password='123', first_name='ali',
                                   last_name='na')
        user2 = User.objects.create(username='mohammad', password='123', first_name='mohammad',
                                   last_name='na')
        question1 = Question.objects.create(text='2+2=', owner=user1, true_answer=3)
        quiz1 = Quiz.objects.create(title='quiz1', designer=user1, duration=1,
                                    is_published=True, answer_published=False)
        quiz1.questions.add(question1)
        quiz_answer1 = QuizAnswer.objects.create(user=user1, quiz=quiz1, percent=100,
                                                 answer_duration=20)
        QuestionAnswer.objects.create(question=question1, quiz=quiz1, quiz_answer=quiz_answer1,
                                        user_answer=3, is_answered=True, evaluation=True)
        quiz_answer2 = QuizAnswer.objects.create(user=user2, quiz=quiz1, percent=0,
                                                 answer_duration=20)
        QuestionAnswer.objects.create(question=question1, quiz=quiz1, quiz_answer=quiz_answer2,
                                        user_answer=4, is_answered=True, evaluation=True)
    
    def test_edit_question(self):
        question_id = Question.objects.get(text='2+2=').id
        data = {'text': '2+2=', 'true_answe': 4}
        response = self.client.post(f"/edit_question/{question_id}/", data=data)
        response = self.client.get(f"/edit_question/{question_id}/")
        user1 = User.objects.get(username='ali')
        user2 = User.objects.get(username='mohammad')
        quiz_answer1 = QuizAnswer.objects.get(user=user1)
        quiz_answer2 = QuizAnswer.objects.get(user=user2)
        self.assertEqual(quiz_answer1.percent, 0)
        self.assertEqual(quiz_answer2.percent, 100)
        self.assertEqual(response.status_code, 200)

