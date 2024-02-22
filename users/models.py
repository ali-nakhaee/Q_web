from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
