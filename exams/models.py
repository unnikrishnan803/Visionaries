from django.db import models
from django.db.models import Avg
from admissions.models import Student

class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Semester 1", "Semester 2"
    academic_year = models.CharField(max_length=20)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-academic_year', 'name']

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class Subject(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    credits = models.IntegerField(default=3)
    course_type = models.CharField(max_length=20, choices=[
        ('Core', 'Core Subject'),
        ('Elective', 'Elective Subject'),
        ('Practical', 'Practical/Lab'),
    ], default='Core')

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

class SemesterResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='semester_results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()  # Out of 100
    grade_points = models.FloatField()  # GPA points (0-4)
    grade = models.CharField(max_length=2)  # Letter grade (A, B, C, D, F)
    credits_earned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'semester', 'subject']
        ordering = ['-semester__academic_year', 'semester__name', 'subject__code']

    def save(self, *args, **kwargs):
        # Calculate grade points and letter grade based on marks
        self.grade_points = self.calculate_grade_points()
        self.grade = self.calculate_letter_grade()
        self.credits_earned = self.subject.credits
        super().save(*args, **kwargs)

        # Update student's CGPA
        self.student.update_cgpa()

    def calculate_grade_points(self):
        """Convert marks to grade points (4.0 scale)"""
        if self.marks_obtained >= 90:
            return 4.0
        elif self.marks_obtained >= 80:
            return 3.7
        elif self.marks_obtained >= 70:
            return 3.3
        elif self.marks_obtained >= 60:
            return 3.0
        elif self.marks_obtained >= 50:
            return 2.7
        elif self.marks_obtained >= 40:
            return 2.3
        else:
            return 0.0

    def calculate_letter_grade(self):
        """Convert marks to letter grade"""
        if self.marks_obtained >= 90:
            return 'A'
        elif self.marks_obtained >= 80:
            return 'B'
        elif self.marks_obtained >= 70:
            return 'C'
        elif self.marks_obtained >= 60:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.student.name} - {self.subject.code}: {self.marks_obtained} ({self.grade})"

class Exam(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.subject

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.IntegerField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.name} - {self.exam.subject}: {self.marks}"
