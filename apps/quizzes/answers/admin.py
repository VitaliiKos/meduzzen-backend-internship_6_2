from django.contrib import admin

from .models import AnswerModel


class AnswerModelAdmin(admin.ModelAdmin):
    verbose_name_plural = "Question answers"

    list_display = ('id', 'question', 'answer_text', 'is_correct')
    list_filter = ('question',)
    search_fields = ('answer_text',)


admin.site.register(AnswerModel, AnswerModelAdmin)
