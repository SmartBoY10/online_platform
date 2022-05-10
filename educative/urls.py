from django.urls import path

from .views import *

urlpatterns = [
    path('courses/', course_list),
    path('resgister-student/', register_student),
    path('student-dashboard/', student_dashboard),
    path('resgister-teacher/', teacher_register),
    path('teacher-dashboard/', teacher_dashboard),
    path('admin/unaprroved-teachers/', admin_unapproved_list),
    path('admin/confirm/<int:pk>/', admin_confirm),
    path('admin/dashboard/', admin_dashboard),
]