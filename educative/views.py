from re import A
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

class CourseListView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseListSerializers(courses, many=True)
        return Response(serializer.data)