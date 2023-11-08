from django.contrib import admin

from .models import QuizResultModel


class QuizResultModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Quizzes Workflow"

    list_display = ('user', 'company', 'quiz', 'score', 'status')
    list_filter = ('status', 'company')
    search_fields = ('user__email', 'company__name', 'quiz__title')
    list_per_page = 20
    ordering = ('-created_at',)


admin.site.register(QuizResultModel, QuizResultModelAdmin)
