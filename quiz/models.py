from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Question(models.Model):
    """ A question with its answer."""
    text = models.TextField()
    true_answer = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the question."""
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
        """Return a string representation of the quiz."""
        return self.title


class QuestionAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user_answer = models.FloatField()
    is_answered = models.BooleanField()
    evaluation = models.BooleanField()
