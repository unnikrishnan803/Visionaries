from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

COURSE_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Information Technology', 'Information Technology'),
    ('Business Administration', 'Business Administration'),
    ('Engineering', 'Engineering'),
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('English Literature', 'English Literature'),
    ('History', 'History'),
]

CAREER_PATH_CHOICES = [
    ('Software Developer', 'Software Developer'),
    ('Data Scientist', 'Data Scientist'),
    ('Business Analyst', 'Business Analyst'),
    ('Engineer', 'Engineer'),
    ('Research Scientist', 'Research Scientist'),
    ('Teacher/Educator', 'Teacher/Educator'),
    ('Entrepreneur', 'Entrepreneur'),
    ('Healthcare Professional', 'Healthcare Professional'),
    ('Creative Professional', 'Creative Professional'),
    ('Management Professional', 'Management Professional'),
]

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    institution_type = models.CharField(max_length=10, choices=[('School', 'School'), ('College', 'College')], default='College')
    institution_name = models.CharField(max_length=100, blank=True)
    grade = models.IntegerField(choices=[(i, str(i)) for i in range(1, 13)], blank=True, null=True)
    level = models.CharField(max_length=2, choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')], blank=True, null=True)
    degree = models.CharField(max_length=10, choices=[('BTech', 'BTech'), ('BCA', 'BCA'), ('BSc', 'BSc'), ('MTech', 'MTech'), ('MCA', 'MCA'), ('MSc', 'MSc')], blank=True, null=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    age = models.IntegerField(default=18)
    date_of_birth = models.DateField(default='2000-01-01')
    guardian_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")

    # Academic Performance Fields
    cgpa = models.FloatField(default=0.0, help_text="Cumulative Grade Point Average")
    total_credits = models.IntegerField(default=0, help_text="Total credits earned")

    # AI Analytics Fields
    dropout_risk_score = models.FloatField(default=0.0, help_text="AI-calculated dropout risk (0-1)")
    performance_forecast = models.FloatField(default=0.0, help_text="Predicted final GPA")
    recommended_career_path = models.CharField(max_length=50, choices=CAREER_PATH_CHOICES, blank=True, null=True)
    attendance_pattern_score = models.FloatField(default=0.0, help_text="Attendance pattern analysis score")

    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate student ID: STU + year + 4-digit number
            year = timezone.now().year
            last_student = Student.objects.filter(student_id__startswith=f'STU{year}').order_by('-student_id').first()
            if last_student:
                last_num = int(last_student.student_id[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.student_id = f'STU{year}{new_num:04d}'
        super().save(*args, **kwargs)

    def get_dropout_risk_level(self):
        """Return human-readable dropout risk level"""
        if self.dropout_risk_score >= 0.8:
            return "High Risk"
        elif self.dropout_risk_score >= 0.5:
            return "Medium Risk"
        elif self.dropout_risk_score >= 0.3:
            return "Low Risk"
        else:
            return "Very Low Risk"

    def get_performance_forecast_grade(self):
        """Convert performance forecast to letter grade"""
        if self.performance_forecast >= 3.7:
            return "A"
        elif self.performance_forecast >= 3.0:
            return "B"
        elif self.performance_forecast >= 2.0:
            return "C"
        elif self.performance_forecast >= 1.0:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ], default='Present')
    subject = models.CharField(max_length=100, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date', 'subject']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class PerformanceAnalytics(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='analytics')
    current_gpa = models.FloatField(default=0.0)
    total_credits = models.IntegerField(default=0)
    completed_subjects = models.IntegerField(default=0)
    average_attendance = models.FloatField(default=0.0)
    study_hours_per_week = models.IntegerField(default=0)
    extracurricular_activities = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    # AI Predictions
    predicted_final_gpa = models.FloatField(default=0.0)
    dropout_probability = models.FloatField(default=0.0)
    recommended_interventions = models.TextField(default='', blank=True)
    career_recommendations = models.TextField(default='', blank=True)

    def __str__(self):
        return f"Analytics for {self.student.name}"

    def calculate_dropout_risk(self):
        """Simple AI algorithm for dropout risk prediction"""
        risk_score = 0.0

        # Attendance factor (30% weight)
        if self.average_attendance < 60:
            risk_score += 0.3
        elif self.average_attendance < 75:
            risk_score += 0.15

        # GPA factor (40% weight)
        if self.current_gpa < 2.0:
            risk_score += 0.4
        elif self.current_gpa < 2.5:
            risk_score += 0.2
        elif self.current_gpa < 3.0:
            risk_score += 0.1

        # Study hours factor (20% weight)
        if self.study_hours_per_week < 5:
            risk_score += 0.2
        elif self.study_hours_per_week < 10:
            risk_score += 0.1

        # Extracurricular factor (10% weight)
        if self.extracurricular_activities == 0:
            risk_score += 0.1

        return min(risk_score, 1.0)  # Cap at 1.0

    def predict_final_performance(self):
        """Simple performance forecasting algorithm"""
        base_prediction = self.current_gpa

        # Attendance bonus/penalty
        attendance_factor = (self.average_attendance - 75) * 0.01  # ±0.25 for 75% attendance
        base_prediction += attendance_factor

        # Study hours bonus
        study_bonus = min(self.study_hours_per_week * 0.02, 0.3)  # Max +0.3 for 15+ hours
        base_prediction += study_bonus

        # Extracurricular bonus
        activity_bonus = min(self.extracurricular_activities * 0.05, 0.2)  # Max +0.2 for 4+ activities
        base_prediction += activity_bonus

        return max(0.0, min(4.0, base_prediction))  # Cap between 0-4.0

    def recommend_career_path(self):
        """AI-based career path recommendations"""
        recommendations = []
        course = self.student.course or ''

        # Computer Science paths
        if course == 'Computer Science':
            if self.current_gpa >= 3.5 and self.study_hours_per_week >= 15:
                recommendations.extend(['Software Developer', 'Data Scientist'])
            elif self.extracurricular_activities >= 2:
                recommendations.append('Entrepreneur')
            else:
                recommendations.append('Software Developer')

        # Engineering paths
        elif course == 'Engineering':
            recommendations.extend(['Engineer', 'Research Scientist'])

        # Business paths
        elif course == 'Business Administration':
            if self.extracurricular_activities >= 3:
                recommendations.extend(['Entrepreneur', 'Management Professional'])
            else:
                recommendations.append('Business Analyst')

        # Science paths
        elif any(subject in course for subject in ['Mathematics', 'Physics', 'Chemistry', 'Biology']):
            recommendations.extend(['Research Scientist', 'Teacher/Educator'])

        # Arts/Humanities paths
        elif any(subject in course for subject in ['English Literature', 'History']):
            recommendations.extend(['Teacher/Educator', 'Creative Professional'])

        # Default recommendations if no specific course match
        if not recommendations:
            if self.current_gpa >= 3.5:
                recommendations.extend(['Research Scientist', 'Professional'])
            elif self.extracurricular_activities >= 2:
                recommendations.append('Entrepreneur')
            else:
                recommendations.append('Professional')

        return recommendations[:3]  # Return top 3 recommendations

    def update_analytics(self):
        """Update all AI predictions"""
        try:
            self.dropout_probability = self.calculate_dropout_risk()
            self.predicted_final_gpa = self.predict_final_performance()
            self.career_recommendations = self.recommend_career_path()

            # Generate intervention recommendations
            interventions = []
            if self.dropout_probability > 0.5:
                interventions.append("Schedule counseling session")
            if self.average_attendance < 70:
                interventions.append("Improve attendance monitoring")
            if self.current_gpa < 2.5:
                interventions.append("Provide academic tutoring")
            if self.study_hours_per_week < 10:
                interventions.append("Recommend study schedule")
    
            # Convert to JSON strings for TextField storage
            import json
            self.recommended_interventions = json.dumps(interventions)
            self.career_recommendations = json.dumps(self.career_recommendations)
            self.save()
    
            # Update student model
            self.student.dropout_risk_score = self.dropout_probability
            self.student.performance_forecast = self.predicted_final_gpa
            if self.career_recommendations:
                try:
                    career_list = json.loads(self.career_recommendations)
                    if career_list:
                        self.student.recommended_career_path = career_list[0]
                except:
                    pass
            self.student.save()
        except Exception as e:
            print(f"Error in update_analytics for student {self.student.name}: {e}")
            raise

    def update_cgpa(self):
        """Calculate and update student's CGPA"""
        from exams.models import SemesterResult

        # Get all semester results for this student
        results = SemesterResult.objects.filter(student=self)

        if results.exists():
            # Calculate CGPA: (sum of grade_points * credits) / total_credits
            total_weighted_points = sum(result.grade_points * result.credits_earned for result in results)
            total_credits = sum(result.credits_earned for result in results)

            if total_credits > 0:
                cgpa = total_weighted_points / total_credits
                self.cgpa = round(cgpa, 2)
            else:
                self.cgpa = 0.0

            # Update total credits
            self.total_credits = total_credits
            self.save()
        else:
            self.cgpa = 0.0
            self.total_credits = 0
            self.save()
