from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.TEACHER:
            group = Group.objects.get(name='teachers')
            group.user_set.add(self)
        elif self.role == self.STUDENT:
            group = Group.objects.get(name='students')
            group.user_set.add(self)
