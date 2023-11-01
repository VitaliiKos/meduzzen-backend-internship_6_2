from django.contrib import admin
from .models import QuestionModel


class QuestionModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Quizz questions"

    list_display = ('id', 'quiz', 'question_text')
    list_filter = ('quiz',)
    search_fields = ('question_text',)


admin.site.register(QuestionModel, QuestionModelAdmin)
