from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admissions.models import Student, PerformanceAnalytics, Attendance
from admissions.forms import StudentForm

@login_required
def profile(request):
    if request.user.groups.filter(name='Student').exists():
        # Student profile
        try:
            student = request.user.student
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard:dashboard')

        if request.method == 'POST':
            form = StudentForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('main:profile')
        else:
            form = StudentForm(instance=student)

        # Get analytics and attendance data
        try:
            analytics = PerformanceAnalytics.objects.get(student=student)
        except PerformanceAnalytics.DoesNotExist:
            analytics = None

        attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:10]  # Last 10 records
        attendance_percentage = 0
        if attendance_records.exists():
            present_count = attendance_records.filter(status='Present').count()
            attendance_percentage = (present_count / attendance_records.count()) * 100

        return render(request, 'main/profile.html', {
            'student': student,
            'form': form,
            'is_student': True,
            'analytics': analytics,
            'attendance_records': attendance_records,
            'attendance_percentage': attendance_percentage
        })
    else:
        # Staff profile - basic user info
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('main:profile')

        return render(request, 'main/profile.html', {
            'user': request.user,
            'is_student': False
        })

def home(request):
    return render(request, 'main/home.html')
