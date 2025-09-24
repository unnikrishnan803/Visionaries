from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admissions.models import Student, PerformanceAnalytics, Attendance
from fees.models import FeePayment
from hostel.models import Room, HostelAllocation
from exams.models import Exam, Mark
from datetime import date, timedelta
from django.db.models import Sum, Avg, Count
from django.utils import timezone

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Student').exists():
        # student dashboard
        try:
            student = request.user.student
        except Student.DoesNotExist:
            return render(request, 'dashboard/no_student.html')
        # get data
        fees = FeePayment.objects.filter(student=student)
        total_paid = sum(f.amount for f in fees)
        balance = 50000 - total_paid  # assume total fee
        # hostel
        try:
            allocation = HostelAllocation.objects.get(student=student)
            room = allocation.room
        except HostelAllocation.DoesNotExist:
            room = None
        # exams
        marks = Mark.objects.filter(student=student)
        next_exam = Exam.objects.filter(date__gte=date.today()).first()

        # AI Analytics for student
        try:
            analytics = student.analytics
            dropout_risk = student.get_dropout_risk_level()
            predicted_grade = student.get_performance_forecast_grade()
            career_paths = analytics.career_recommendations[:3] if analytics.career_recommendations else []
            dropout_percentage = int(analytics.dropout_probability * 100) if analytics else 0
        except:
            analytics = None
            dropout_risk = "Calculating..."
            predicted_grade = "N/A"
            career_paths = []
            dropout_percentage = 0

        context = {
            'student': student,
            'total_paid': total_paid,
            'balance': balance,
            'room': room,
            'marks': marks,
            'next_exam': next_exam,
            # AI Analytics
            'analytics': analytics,
            'dropout_risk': dropout_risk,
            'predicted_grade': predicted_grade,
            'career_paths': career_paths,
            'dropout_percentage': dropout_percentage,
        }
        return render(request, 'dashboard/student_dashboard.html', context)
    else:
        # staff/admin/institution dashboard
        today = timezone.now()
        students = Student.objects.all()
        pending_admissions = students.filter(status='Pending').count()
        fees = FeePayment.objects.all()
        fees_month = fees.filter(paid_on__month=today.month, paid_on__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0
        rooms = Room.objects.all()
        allocations = HostelAllocation.objects.all()
        hostel_occupancy = allocations.count() / rooms.count() * 100 if rooms.count() > 0 else 0
        exams = Exam.objects.all()
        upcoming_exams = exams.filter(date__gte=today.date())[:5]
        marks = Mark.objects.all()

        # AI Analytics Data
        analytics = PerformanceAnalytics.objects.all()
        high_risk_students = students.filter(dropout_risk_score__gte=0.7).count()
        avg_gpa = analytics.aggregate(Avg('current_gpa'))['current_gpa__avg'] or 0
        avg_attendance = analytics.aggregate(Avg('average_attendance'))['average_attendance__avg'] or 0

        # Recent attendance data (last 7 days)
        week_ago = today - timedelta(days=7)
        recent_attendance = Attendance.objects.filter(date__gte=week_ago)
        attendance_summary = recent_attendance.values('status').annotate(count=Count('status'))

        # Students needing intervention
        intervention_needed = students.filter(dropout_risk_score__gte=0.5)[:5]

        # Calculate percentages for template
        for student in intervention_needed:
            student.dropout_percentage = int(student.dropout_risk_score * 100)

        context = {
            'student_count': students.count(),
            'pending_admissions': pending_admissions,
            'fee_count': fees.count(),
            'fees_month': fees_month,
            'room_count': rooms.count(),
            'allocation_count': allocations.count(),
            'hostel_occupancy': round(hostel_occupancy, 1),
            'exam_count': exams.count(),
            'mark_count': marks.count(),
            'students': students[:10],  # recent
            'fees': fees[:10],
            'upcoming_exams': upcoming_exams,
            # AI Analytics
            'high_risk_students': high_risk_students,
            'avg_gpa': round(avg_gpa, 2),
            'avg_attendance': round(avg_attendance, 1),
            'intervention_needed': intervention_needed,
            'attendance_summary': attendance_summary,
        }
        return render(request, 'dashboard/staff_dashboard.html', context)
