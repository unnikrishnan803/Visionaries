from django import forms
from .models import Student, Attendance, PerformanceAnalytics

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'institution_type', 'institution_name', 'grade', 'level', 'degree', 'course', 'age', 'date_of_birth', 'guardian_name', 'phone', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        institution_type = cleaned_data.get('institution_type')
        grade = cleaned_data.get('grade')
        level = cleaned_data.get('level')
        degree = cleaned_data.get('degree')

        if institution_type == 'School':
            if not grade:
                raise forms.ValidationError("Grade is required for school students.")
        elif institution_type == 'College':
            if not level:
                raise forms.ValidationError("Level is required for college students.")
            if not degree:
                raise forms.ValidationError("Degree is required for college students.")

        return cleaned_data

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status', 'subject']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PerformanceAnalyticsForm(forms.ModelForm):
    class Meta:
        model = PerformanceAnalytics
        fields = ['current_gpa', 'average_attendance', 'study_hours_per_week', 'extracurricular_activities']
        widgets = {
            'current_gpa': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '4.0'}),
            'average_attendance': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '100'}),
        }