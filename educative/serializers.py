from rest_framework import serializers

from .models import *


class TeacherSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):

    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Student
        fields = '__all__'