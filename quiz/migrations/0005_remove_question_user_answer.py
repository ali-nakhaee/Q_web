# Generated by Django 4.2.10 on 2024-02-17 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_alter_question_user_answer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="user_answer",
        ),
    ]
