# Generated by Django 4.2.10 on 2024-03-05 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0006_rename_quiz_id_questionanswer_quiz"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionanswer",
            name="user_answer",
            field=models.FloatField(null=True),
        ),
    ]