from django.db import models


class Term(models.Model):
    class TERM_NAME(models.TextChoices):
        FIRST_TERM = "FIRST TERM", "FIRST TERM"
        SECOND_TERM = "SECOND TERM", "SECOND TERM"
        THIRD_TERM = "THIRD TERM", "THIRD TERM"

    term = models.CharField(max_length=20, choices=TERM_NAME.choices)
    session = models.CharField(
        max_length=9, help_text="Enter the section in the format 'YYYY/YYYY'"
    )

    def __str__(self):
        return f"{self.term} - {self.session}"
