from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Question(models.Model):
    text = models.TextField()
    true_answer = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    designer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField(Question)
    duration = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'quizzes'


class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    percent = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    answer_duration = models.PositiveIntegerField()
    date_answered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.quiz.title


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE)
    user_answer = models.FloatField(null=True)
    is_answered = models.BooleanField()
    evaluation = models.BooleanField()

    def __str__(self):
        return self.question.text + " - " + self.quiz.title
