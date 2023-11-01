from django.contrib import admin

from .models import QuizModel


class QuizModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Quizzes"

    list_display = ('title', 'frequency', 'user', 'company')
    list_filter = ('user', 'company')
    search_fields = ('title', 'id', 'company__name')


admin.site.register(QuizModel, QuizModelAdmin)
