from django.db import models


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    difficulty = models.CharField(max_length=15)
    price = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.username