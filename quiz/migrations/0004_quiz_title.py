# Generated by Django 4.2.10 on 2024-02-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0003_rename_owner_quiz_designer_quiz_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="title",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
