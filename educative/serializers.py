from rest_framework import serializers

from .models import *


class TeacherDetailSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Teacher
        fields = ("user", "status")


class CourseListSerializers(serializers.ModelSerializer):

    teacher = TeacherDetailSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ("name", "description", "teacher", "get_students_count")


class StudentDetailSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Student
        fields = ("user", "courses")


class AdminDashboardSerializer(serializers.Serializer):
    teacher = serializers.CharField(max_length=35)
    course = serializers.CharField(max_length=50)
    count_of_students = serializers.IntegerField()
