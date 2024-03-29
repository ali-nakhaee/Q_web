# Generated by Django 4.2.10 on 2024-03-26 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("quiz", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="quizanswer",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="designer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="quiz",
            name="questions",
            field=models.ManyToManyField(to="quiz.question"),
        ),
        migrations.AddField(
            model_name="questionanswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="quiz.question"
            ),
        ),
        migrations.AddField(
            model_name="questionanswer",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.quiz"
            ),
        ),
        migrations.AddField(
            model_name="questionanswer",
            name="quiz_answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="quiz.quizanswer"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
