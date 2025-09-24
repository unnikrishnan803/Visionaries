from django import forms
from .models import Exam, Mark, Semester, Subject, SemesterResult
from admissions.models import Student

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name', 'academic_year', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'semester', 'credits', 'course_type']

class SemesterResultForm(forms.ModelForm):
    class Meta:
        model = SemesterResult
        fields = ['student', 'semester', 'subject', 'marks_obtained']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(status='Approved')
        self.fields['semester'].queryset = Semester.objects.all()
        self.fields['subject'].queryset = Subject.objects.all()

class BulkSemesterResultForm(forms.Form):
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(),
        empty_label="Select Semester"
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(status='Approved'),
        empty_label="Select Student"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'semester' in self.data:
            try:
                semester_id = int(self.data.get('semester'))
                self.fields['subjects'] = forms.ModelMultipleChoiceField(
                    queryset=Subject.objects.filter(semester_id=semester_id),
                    widget=forms.CheckboxSelectMultiple,
                    required=False
                )
            except (ValueError, TypeError):
                pass

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['subject', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'exam', 'marks', 'grade']
        widgets = {
            'marks': forms.NumberInput(attrs={'min': 0, 'max': 100}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all()
        self.fields['exam'].queryset = Exam.objects.all()