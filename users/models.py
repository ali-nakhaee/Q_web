from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            # "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            "کاراکترهای مجاز: حروف انگلیسی، اعداد و @/./+/-/_"
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'

    ROLE_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )

    first_name = models.CharField(max_length=150,
                                  help_text="از نام اصلی خود استفاده کنید.")
    last_name = models.CharField(max_length=150,
                                 help_text="از نام خانوادگی اصلی خود استفاده کنید.")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=STUDENT)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.TEACHER:
            group = Group.objects.get(name='teachers')
            group.user_set.add(self)
        elif self.role == self.STUDENT:
            group = Group.objects.get(name='students')
            group.user_set.add(self)
