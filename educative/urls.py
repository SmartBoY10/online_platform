from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
]