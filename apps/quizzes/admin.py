from django.contrib import admin

from .models import AnswerModel, QuestionModel, QuizModel


class QuizModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Quizzes"

    list_display = ('title', 'frequency', 'user', 'company')
    list_filter = ('user', 'company')
    search_fields = ('title', 'id', 'company__name')
    ordering = ('-created_at',)


class QuestionModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Quizz questions"

    list_display = ('id', 'quiz', 'question_text')
    list_filter = ('quiz',)
    search_fields = ('question_text',)
    ordering = ('id',)


class AnswerModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Question answers"

    list_display = ('id', 'question', 'answer_text', 'is_correct')
    list_filter = ('question',)
    search_fields = ('answer_text',)
    ordering = ('id',)


admin.site.register(AnswerModel, AnswerModelAdmin)
admin.site.register(QuestionModel, QuestionModelAdmin)
admin.site.register(QuizModel, QuizModelAdmin)
