from django.contrib import admin
from .models import Quiz, Question, Option, QuizSession, StudentResponse, Result


class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  # Number of empty forms to display for adding options


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of empty forms to display for adding questions


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "subject", "created_at")
    search_fields = ("name",)
    list_filter = ("type", "subject")
    inlines = [QuestionInline]  # Inline for questions


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "quiz")
    search_fields = ("text",)
    list_filter = ("quiz",)
    inlines = [OptionInline]  # Inline for options


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "is_correct", "question")
    search_fields = ("text",)
    list_filter = ("is_correct", "question")


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "start_time", "end_time", "status")
    search_fields = ("quiz__name",)
    list_filter = ("status", "quiz")


@admin.register(StudentResponse)
class StudentResponseAdmin(admin.ModelAdmin):
    list_display = ("student", "session", "question", "selected_option", "score")
    search_fields = ("student__first_name", "student__last_name", "session__code")
    list_filter = ("session",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "response",
        "correct",
        "failed",
        "total_questions",
        "percentage",
    )
    search_fields = ("response__student__first_name", "response__student__last_name")
    list_filter = ("session",)
