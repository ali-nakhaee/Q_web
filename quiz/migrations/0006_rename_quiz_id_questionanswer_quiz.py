# Generated by Django 4.2.10 on 2024-03-05 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0005_quiz_date_added"),
    ]

    operations = [
        migrations.RenameField(
            model_name="questionanswer",
            old_name="quiz_id",
            new_name="quiz",
        ),
    ]