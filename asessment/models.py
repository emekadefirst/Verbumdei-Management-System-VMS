import uuid
from django.db import models
from django.utils import timezone
from student.models import Student
from grade.models import Subject
from term.models.term import Term
from django.db.models import Sum


def exam_code():
    return f"OT{str(uuid.uuid4())[:8]}"


class Quiz(models.Model):
    class QUIZ_TYPE(models.TextChoices):
        EXAMINATION = "EXAMINATION", "Examination"
        CONTINUOUS_ASSESSMENT = "CONTINUOUS_ASSESSMENT", "Continuous assessment"
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=25, choices=QUIZ_TYPE.choices)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=55, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.subject:
            self.name = self.subject.name
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.subject.name} {self.type}"

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()


    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class QuizSession(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = "NOT STARTED", "Not Started"
        ONGOING = "ONGOING", "Ongoing"
        ENDED = "ENDED", "Ended"
    id = models.AutoField(primary_key=True)
    students = models.ManyToManyField(Student)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    code = models.CharField(max_length=30, default=exam_code, unique=True)
    duration = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)

    class Meta:
        ordering = ['-start_time']
    def __str__(self):
        return self.code

    def is_time_limit_exceeded(self):
        if self.end_time == timezone.now():
            raise ValueError("Session Time out, reschedule")
        return self


class StudentResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.student in self.session:
            correct_option = self.question.options.filter(is_correct=True).first()
            if correct_option and self.selected_option == correct_option:
                self.score = 1
            else:
                self.score = 0
            raise ValueError(f"This student wasn't assigned for the test {self.session.students}")
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['session', 'question', 'selected_option']


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    response = models.ForeignKey(StudentResponse, on_delete=models.CASCADE)
    correct = models.PositiveIntegerField(default=0, null=True, blank=True)
    failed = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_questions = models.PositiveIntegerField(default=0, null=True, blank=True)
    percentage = models.PositiveIntegerField(default=0, null=True, blank=True)

    @classmethod
    def calculate_result(cls, student, session):
        responses = StudentResponse.objects.filter(student=student, session=session)

        total_questions = responses.count()
        correct = responses.filter(score=1).count()
        failed = total_questions - correct if total_questions else 0
        percentage = (correct / total_questions * 100) if total_questions > 0 else 0

        result, _ = cls.objects.update_or_create(
            session=session,
            response__student=student,
            defaults={
                'correct': correct,
                'failed': failed,
                'total_questions': total_questions,
                'percentage': percentage
            }
        )
        return result

    @property
    def quiz_name(self):
        return self.session.quiz.name

    @property
    def student(self):
        full_name = f"{self.response.student.first_name} {self.response.student.last_name}"
        return full_name
