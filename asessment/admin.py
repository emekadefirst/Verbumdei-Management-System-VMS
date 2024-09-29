from django.contrib import admin
from django.utils.html import format_html
from .models import Quiz, Question, Option, QuizAttempt, StudentAnswer

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('text', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('text', 'quiz__title')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('subject', 'type', 'is_active', 'time_limit', 'created_at')
    list_filter = ('type', 'is_active', 'created_at')
    search_fields = ['subject']
    inlines = [QuestionInline]
    

class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option')
    can_delete = False

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score', 'percentage', 'completed_at')
    list_filter = ('quiz', 'completed_at')
    search_fields = ('student__user__username', 'quiz__title')
    readonly_fields = ('score', 'percentage')
    inlines = [StudentAnswerInline]

    def percentage(self, obj):
        total_questions = obj.quiz.questions.count()
        if total_questions > 0:
            percentage = (obj.score / total_questions) * 100
            return format_html('<span style="color: {};">{:.2f}%</span>', 
                               'green' if percentage >= 70 else 'red', percentage)
        return "N/A"
    percentage.short_description = 'Percentage'

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text', 'question__text')

admin.site.register(Question, QuestionAdmin)