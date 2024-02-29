from django.contrib import admin

from .models import Question, Quiz, QuestionAnswer

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuestionAnswer)
