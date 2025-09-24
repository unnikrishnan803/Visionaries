from django import forms
from django.db import models
from .models import Room, HostelAllocation, StaffAllocation
from admissions.models import Student
from django.contrib.auth.models import User

class StudentAllocationForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.filter(status='Approved'), empty_label="Select Student")

    class Meta:
        model = HostelAllocation
        fields = ['student', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show rooms with available capacity
        self.fields['room'].queryset = Room.objects.filter(occupied__lt=models.F('capacity'))

class StaffAllocationForm(forms.ModelForm):
    staff = forms.ModelChoiceField(queryset=User.objects.exclude(groups__name='Student'), empty_label="Select Staff")

    class Meta:
        model = StaffAllocation
        fields = ['staff', 'room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show rooms with available capacity
        self.fields['room'].queryset = Room.objects.filter(occupied__lt=models.F('capacity'))