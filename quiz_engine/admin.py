from django.contrib import admin
from .models import Subject, Quiz, Question, Answer, Assignment

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'passing_score')
    list_filter = ('subject',)
    search_fields = ('title', 'subject__name')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text')
    list_filter = ('quiz__subject', 'quiz')
    search_fields = ('question_text', 'quiz__title')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('answer_text', 'question__question_text')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'status', 'score', 'assigned_at', 'completed_at')
    list_filter = ('status', 'quiz__subject', 'assigned_at')
    search_fields = ('user__username', 'quiz__title', 'quiz__subject__name')
    readonly_fields = ('assigned_at', 'completed_at')

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Assignment, AssignmentAdmin)
