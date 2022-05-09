import re
from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UnapprovedTeachers(models.Model):
    teacher = models.ManyToManyField(Teacher)


class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    difficulty = models.CharField(max_length=15)
    price = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_students_count(self):
        students_count = Student.objects.filter(courses__name=self.name).count()
        return students_count


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.username