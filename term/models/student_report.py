# from django.db import models
# from student.models import Student
# from grade.models import Subject, Class
# from asessment.models import QuizAttempt, Quiz


# class SubjectResult(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="subject_results"
#     )
#     subject = models.ForeignKey(
#         Subject, on_delete=models.CASCADE, related_name="subject_results"
#     )
#     ca_attempt = models.ForeignKey(
#         QuizAttempt,
#         on_delete=models.CASCADE,
#         related_name="ca_subject_results",
#         null=True,
#         blank=True,
#     )
#     exam_attempt = models.ForeignKey(
#         QuizAttempt,
#         on_delete=models.CASCADE,
#         related_name="exam_subject_results",
#         null=True,
#         blank=True,
#     )

#     @property
#     def ca_score(self):
#         if (
#             self.ca_attempt
#             and self.ca_attempt.quiz.type == Quiz.QUIZ_TYPE.CONTINUOUS_ASSESSMENT
#         ):
#             return self.ca_attempt.score
#         return 0

#     @property
#     def examination_score(self):
#         if (
#             self.exam_attempt
#             and self.exam_attempt.quiz.type == Quiz.QUIZ_TYPE.EXAMINATION
#         ):
#             return self.exam_attempt.score
#         return 0

#     @property
#     def total_score(self):
#         return self.ca_score + self.examination_score

#     def __str__(self):
#         return f"{self.student} - {self.subject.name}"


# class Report(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="reports"
#     )
#     class_group = models.ForeignKey(
#         Class, on_delete=models.CASCADE, related_name="reports"
#     )
#     subjects = models.ManyToManyField(Subject, through="SubjectResult")
#     created_at = models.DateTimeField(auto_now_add=True)

#     @property
#     def total_ca_score(self):
#         total = sum(result.ca_score for result in self.subject_results.all())
#         return total

#     @property
#     def total_exam_score(self):
#         total = sum(result.examination_score for result in self.subject_results.all())
#         return total

#     @property
#     def overall_total_score(self):
#         return self.total_ca_score + self.total_exam_score

#     def generate_report(self):
#         return {
#             "student": self.student.full_name,
#             "class": self.class_group.name,
#             "subjects": [
#                 {
#                     "subject": result.subject.name,
#                     "ca_score": result.ca_score,
#                     "exam_score": result.examination_score,
#                     "total_score": result.total_score,
#                 }
#                 for result in self.subject_results.all()
#             ],
#             "total_ca_score": self.total_ca_score,
#             "total_exam_score": self.total_exam_score,
#             "overall_total_score": self.overall_total_score,
#         }

#     def __str__(self):
#         return f"Report for {self.student} in {self.class_group.name}"


