from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Exam, Mark, Semester, Subject, SemesterResult
from .forms import ExamForm, MarkForm, SemesterForm, SubjectForm, SemesterResultForm, BulkSemesterResultForm
from admissions.models import Student

@login_required
def exams(request):
    from .forms import ExamForm, MarkForm, SemesterForm, SubjectForm, SemesterResultForm
    from admissions.models import Student

    is_student = request.user.groups.filter(name='Student').exists()

    if is_student:
        # Student view
        try:
            student = request.user.student
        except:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard:dashboard')

        # Show only upcoming exams and student's marks
        exams = Exam.objects.filter(date__gte=timezone.now().date()).order_by('date')
        marks = Mark.objects.filter(student=student).select_related('exam')

        # Get semester results and CGPA
        semester_results = SemesterResult.objects.filter(student=student).select_related('semester', 'subject')
        cgpa = student.cgpa
        total_credits = student.total_credits

        return render(request, 'exams/exams.html', {
            'exams': exams,
            'marks': marks,
            'semester_results': semester_results,
            'student': student,
            'cgpa': cgpa,
            'total_credits': total_credits,
            'is_student': True
        })
    else:
        # Staff view
        if request.method == 'POST':
            if 'add_exam' in request.POST:
                exam_form = ExamForm(request.POST)
                if exam_form.is_valid():
                    exam_form.save()
                    messages.success(request, 'Exam added successfully.')
                    return redirect('exams:exams')
            elif 'add_mark' in request.POST:
                mark_form = MarkForm(request.POST)
                if mark_form.is_valid():
                    mark_form.save()
                    messages.success(request, 'Mark added successfully.')
                    return redirect('exams:exams')
            elif 'add_semester' in request.POST:
                semester_form = SemesterForm(request.POST)
                if semester_form.is_valid():
                    semester_form.save()
                    messages.success(request, 'Semester added successfully.')
                    return redirect('exams:exams')
            elif 'add_subject' in request.POST:
                subject_form = SubjectForm(request.POST)
                if subject_form.is_valid():
                    subject_form.save()
                    messages.success(request, 'Subject added successfully.')
                    return redirect('exams:exams')
            elif 'add_semester_result' in request.POST:
                result_form = SemesterResultForm(request.POST)
                if result_form.is_valid():
                    result_form.save()
                    messages.success(request, 'Semester result added successfully.')
                    return redirect('exams:exams')
        else:
            exam_form = ExamForm()
            mark_form = MarkForm()
            semester_form = SemesterForm()
            subject_form = SubjectForm()
            result_form = SemesterResultForm()

        exams = Exam.objects.all().order_by('-date')
        marks = Mark.objects.all().select_related('exam', 'student')
        students = Student.objects.all()
        semesters = Semester.objects.all()
        subjects = Subject.objects.all()
        semester_results = SemesterResult.objects.all().select_related('student', 'semester', 'subject')

        return render(request, 'exams/exams.html', {
            'exams': exams,
            'marks': marks,
            'students': students,
            'semesters': semesters,
            'subjects': subjects,
            'semester_results': semester_results,
            'exam_form': exam_form,
            'mark_form': mark_form,
            'semester_form': semester_form,
            'subject_form': subject_form,
            'result_form': result_form,
            'is_student': False
        })

@login_required
def semester_results(request, student_id=None):
    """View semester results for a specific student or all students"""
    is_student = request.user.groups.filter(name='Student').exists()

    if is_student:
        # Students can only see their own results
        try:
            student = request.user.student
        except:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard:dashboard')
    else:
        # Staff can see all or specific student results
        if student_id:
            student = get_object_or_404(Student, id=student_id)
        else:
            student = None

    if student:
        semester_results = SemesterResult.objects.filter(student=student).select_related('semester', 'subject')
        semesters = Semester.objects.filter(
            id__in=semester_results.values_list('semester', flat=True).distinct()
        ).order_by('-academic_year', 'name')

        # Group results by semester
        results_by_semester = {}
        for semester in semesters:
            results_by_semester[semester] = semester_results.filter(semester=semester)

        context = {
            'student': student,
            'results_by_semester': results_by_semester,
            'cgpa': student.cgpa,
            'total_credits': student.total_credits,
            'is_student': is_student
        }
    else:
        # Staff view - show all students with their CGPA
        students_with_cgpa = Student.objects.filter(status='Approved').exclude(cgpa=0).order_by('-cgpa')
        context = {
            'students_with_cgpa': students_with_cgpa,
            'is_student': False
        }

    return render(request, 'exams/semester_results.html', context)

@login_required
def get_subjects_by_semester(request):
    """AJAX endpoint to get subjects for a semester"""
    semester_id = request.GET.get('semester_id')
    if semester_id:
        subjects = Subject.objects.filter(semester_id=semester_id).values('id', 'code', 'name', 'credits')
        return JsonResponse(list(subjects), safe=False)
    return JsonResponse([], safe=False)
