from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """ A question with its answer."""
    text = models.TextField()
    true_answer = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the question."""
        # noinspection PyTypeChecker
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text
