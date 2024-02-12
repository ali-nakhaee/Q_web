from django.db import models


class Question(models.Model):
    """ A question with its answer."""
    text = models.TextField()
    answer = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the question."""
        # noinspection PyTypeChecker
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text
