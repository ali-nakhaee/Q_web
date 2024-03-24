from django.contrib import admin

from .models import Question, Quiz, QuestionAnswer, QuizAnswer

# admin.site.register(Question)
# admin.site.register(Quiz)
# admin.site.register(QuestionAnswer)
# admin.site.register(QuizAnswer)


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz', 'answer_duration', 'percent']
    list_display_links = ['id', 'user', 'quiz']
    sortable_by = ['answer_duration', 'date_answered', 'percent', 'id']
    list_filter = ['quiz']
    fields = [('user', 'quiz'), 'percent']


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'designer', 'title', 'duration']
    inlines = [QuizAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz_answer']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'owner']
