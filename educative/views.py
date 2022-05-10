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
    """Main page uchun kurslarri list"""
    courses = Course.objects.all()
    serializer = CourseSerializers(courses, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def register_student(request):
    """Talaba ro'yxatdan o'tishi uchun"""
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        student = Student.objects.create(user=user)
        serializer = StudentSerializer(student)
        login(request, user)
        return Response(serializer.data)
    else:
        return Response("Registration error")


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def teacher_dashboard(request):
    """Ustoz dashbordi"""
    teacher = get_object_or_404(Teacher, user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    serializer = CourseSerializers(courses, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def course_view(request, pk):
    course = get_object_or_404(Course, id=pk)
    serializer = CourseSerializers(course)
    return Response(serializer.data)


@api_view(["POST"])    
@permission_classes((IsAuthenticated,))
def course_create(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    form = CourseCreateForm(request.POST)
    if form.is_valid():
        course = form.save()
        course.teacher = teacher
        course.save()
        serializer = CourseSerializers(course)
    return Response(serializer.data)


@api_view(["PATCH", "DELETE"])
@permission_classes((IsAuthenticated,))
def course_update(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.method == 'PATCH':
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.description = form.cleaned_data['description']
            course.difficulty = form.cleaned_data['difficulty']
            course.price = form.cleaned_data['price']
            course.save()
            serializer = CourseSerializers(course)
            return Response(serializer.data)
    elif request.method == 'DELETE':
        course.delete()
        return Response("Kurs o'chirildi")

@api_view(["POST"])
def teacher_register(request):
    """Ustoz ro'yxatdan o'tishi uchun"""
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        teacher = Teacher.objects.create(user=user)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
    else:
        return Response("Registration error")


@api_view(["GET"])
@permission_classes((IsAuthenticated, IsAdminUser,))
def admin_unapproved_list(request):
    """Tasdiqlanmagan ustozlar listi"""
    teachers = Teacher.objects.filter(status=False)
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAuthenticated, IsAdminUser,))
def admin_confirm(request, pk):
    """Ustozlarni tasdiqlash"""
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
    """Admin dashbordi"""
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
def student_enroll(request, pk):
    course = get_object_or_404(Course, id=pk)
    student = get_object_or_404(Student, user=request.user)
    course.student_set.add(student)
    student.save()
    serializer = CourseSerializers(student.courses.all(), many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def student_dashboard(request):
    """Student dashbordi"""
    student = get_object_or_404(Student, user=request.user)
    courses = student.courses.all()
    serializer = CourseSerializers(courses, many=True)
    return Response(serializer.data)