from django.contrib import admin

from .models import Question, Quiz, QuestionAnswer, QuizAnswer

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuestionAnswer)
admin.site.register(QuizAnswer)
