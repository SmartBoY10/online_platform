from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from .models import *
from .serializers import *
from .forms import *


@api_view(["GET"])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseListSerializers(courses, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def register_student(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        student = Student.objects.create(user=user)
        serializer = StudentDetailSerializer(student)
        login(request, user)
        messages.success(request, 'You are succes signed up')
        return Response(serializer.data)
    else:
        messages.error(request, 'Registration error')


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def teacher_dashboard(request):
    # teacher=Teacher.objects.get(user=request.user)
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    serializer = CourseListSerializers(courses, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def teacher_register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        teacher = Teacher.objects.create(user=user)
        serializer = TeacherDetailSerializer(teacher)
        messages.success(request, 'You are succes signed up')
        return Response(serializer.data)
    else:
        messages.error(request, 'Registration error')
        return Response("Forma xato")


@api_view(["GET"])
@permission_classes((IsAuthenticated, IsAdminUser,))
def admin_unapproved_list(request):
    teachers = Teacher.objects.filter(status=False)
    serializer = TeacherDetailSerializer(teachers, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated, IsAdminUser,))
def admin_confirm(request, pk):
    teacher = Teacher.objects.get(id=pk)
    if request.GET.get("confirm"):
        teacher.status = True
        teacher.save()
        return Response("Teacher qoshildi")
    else:
        teacher.delete()
        return Response("Udalit qilindi")


@api_view(["GET"])
@permission_classes((IsAuthenticated, IsAdminUser,))
def admin_dashboard(request):
    teachers = Teacher.objects.filter(status=True)
    list_of_data = []
    for teacher in teachers:
        teachers_courses = Course.objects.filter(teacher=teacher)
        obj = {}
        courses = {}
        for course in teachers_courses:
            courses[course.id] = {'course': course.name, 'count': course.get_students_count()}
        
        obj['teacher'] = teacher.user.username
        obj['courses'] = courses
        list_of_data.append(obj)
            
    return Response(list_of_data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    courses = student.courses.all()
    serializer = CourseListSerializers(courses, many=True)
    return Response(serializer.data)