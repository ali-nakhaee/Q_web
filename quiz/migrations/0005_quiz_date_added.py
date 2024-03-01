# Generated by Django 4.2.10 on 2024-03-01 07:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_quiz_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="date_added",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
