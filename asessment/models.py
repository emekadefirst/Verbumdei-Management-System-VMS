from django.db import models
from django.utils import timezone
from student.models import Student
from grade.models import Subject



class Quiz(models.Model):
    class QUIZ_TYPE(models.TextChoices):
        EXAMINATION = "EXAMINATION", "Examination"
        CONTINUOUS_ASSESSMENT = "CONTINUOUS_ASSESSMENT", "Continuous assessment"
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=25, choices=QUIZ_TYPE.choices)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in minutes")
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.subject.name} {self.type}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()


    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return f"{self.student} - {self.quiz.title}"

    def calculate_score(self):
        correct_answers = self.answers.filter(selected_option__is_correct=True).select_related('question')
        total_points = sum(answer.question.points for answer in correct_answers)
        max_points = sum(question.points for question in self.quiz.questions.all())
        self.score = total_points
        self.save()
        return {
            'score': self.score,
            'total': max_points,
            'percentage': (self.score / max_points) * 100 if max_points > 0 else 0
        }

    def is_time_limit_exceeded(self):
        if self.quiz.time_limit:
            time_spent = (timezone.now() - self.start_time).total_seconds() / 60
            return time_spent > self.quiz.time_limit
        return False

    def complete_attempt(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def time_out_attempt(self):
        self.status = 'timed_out'
        self.completed_at = timezone.now()
        self.save()
        
        

class StudentAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz_attempt.student.registration_id} - {self.question.text}"

    class Meta:
        unique_together = ['quiz_attempt', 'question']