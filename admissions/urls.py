from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('', views.admissions, name='admissions'),
    path('edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('attendance/', views.manage_attendance, name='manage_attendance'),
    path('analytics/', views.manage_analytics, name='manage_analytics'),
    path('analytics/<int:student_id>/', views.manage_analytics, name='manage_student_analytics'),
]