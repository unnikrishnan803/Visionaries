from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exams, name='exams'),
    path('semester-results/', views.semester_results, name='semester_results'),
    path('semester-results/<int:student_id>/', views.semester_results, name='student_semester_results'),
    path('api/subjects-by-semester/', views.get_subjects_by_semester, name='get_subjects_by_semester'),
]