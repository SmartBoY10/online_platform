from rest_framework import serializers

from .models import *


class CourseListSerializers(serializers.ModelSerializer):

    teacher = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Course
        fields = ("name", "description", "teacher")