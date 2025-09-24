from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Attendance, PerformanceAnalytics
from .forms import StudentForm, AttendanceForm, PerformanceAnalyticsForm

def admissions(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.status = 'Admitted'
            student.save()
            # Create user account
            user = User.objects.create_user(username=student.student_id, email=student.email, password='student123')
            student.user = user
            student.save()
            # Add to Student group
            student_group, created = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)
            return render(request, 'admissions/admission_success.html', {'student': student})
    else:
        form = StudentForm()
    return render(request, 'admissions/admissions.html', {'form': form})

def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admissions/edit_student.html', {'form': form, 'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('dashboard:dashboard')
    return render(request, 'admissions/delete_student.html', {'student': student})

@login_required
@user_passes_test(lambda u: not u.groups.filter(name='Student').exists())
def manage_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user
            attendance.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('admissions:manage_attendance')
    else:
        form = AttendanceForm()

    # Get recent attendance records
    attendance_records = Attendance.objects.all().order_by('-date')[:50]
    students = Student.objects.all()

    context = {
        'form': form,
        'attendance_records': attendance_records,
        'students': students,
    }
    return render(request, 'admissions/manage_attendance.html', context)

@login_required
@user_passes_test(lambda u: not u.groups.filter(name='Student').exists())
def manage_analytics(request, student_id=None):
    if student_id:
        student = get_object_or_404(Student, id=student_id)
        try:
            analytics = PerformanceAnalytics.objects.get(student=student)
        except PerformanceAnalytics.DoesNotExist:
            analytics = PerformanceAnalytics.objects.create(student=student)

        if request.method == 'POST':
            form = PerformanceAnalyticsForm(request.POST, instance=analytics)
            if form.is_valid():
                try:
                    analytics = form.save()
                    analytics.update_analytics()  # Recalculate AI predictions
                    messages.success(request, f'Analytics updated for {student.name}.')
                    return redirect('admissions:manage_analytics', student_id=student_id)
                except Exception as e:
                    messages.error(request, f'Error updating analytics: {str(e)}')
                    print(f"Analytics update error: {e}")  # Debug print
                    import traceback
                    traceback.print_exc()
        else:
            form = PerformanceAnalyticsForm(instance=analytics)

        context = {
            'form': form,
            'student': student,
            'analytics': analytics,
        }
        return render(request, 'admissions/manage_analytics.html', context)
    else:
        # List all students for analytics management
        students = Student.objects.all().prefetch_related('analytics')
        context = {
            'students': students,
        }
        return render(request, 'admissions/analytics_list.html', context)
