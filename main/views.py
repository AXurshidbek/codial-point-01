from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .permissions import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name']
    ordering_fields = ['id', 'name']
    search_fields = ['name']


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'mentor', 'active', 'created_at']
    ordering_fields = ['id', 'name', 'created_at']
    search_fields = ['name']


class GroupRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class MentorListCreateView(generics.ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]


class MentorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated]


class MentorDetailView(generics.RetrieveAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsMentor]

    def get_object(self):
        return get_object_or_404(Mentor, user=self.request.user)


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['user__username', 'group', 'birth_date','group__mentor']
    ordering_fields = ['id', 'user__username', 'birth_date', 'created_at']
    search_fields = ['user_ _username', 'bio']


class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStudent]

    def get_object(self):
        return get_object_or_404(Student, user=self.request.user)


class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use StudentUpdateSerializer for PUT/PATCH requests
        if self.request.method in ['PUT', 'PATCH']:
            return StudentUpdateSerializer
        # Default to StudentSerializer for other methods like GET, DELETE
        return StudentSerializer


class PointTypeListCreateView(generics.ListCreateAPIView):
    queryset = PointType.objects.all()
    serializer_class = PointTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'max_point']
    ordering_fields = ['id', 'name', 'max_point']
    search_fields = ['name']


class PointTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PointType.objects.all()
    serializer_class = PointTypeSerializer
    permission_classes = [IsAuthenticated]


class GivePointListCreateView(generics.ListCreateAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['mentor', 'student', 'point_type', 'date','student__group']
    ordering_fields = ['id', 'amount', 'date', 'created_at']
    search_fields = ['description']
    pagination_class=CustomLimitOffsetPagination



    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return", type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset', openapi.IN_QUERY, description="The initial index to start returning results from", type=openapi.TYPE_INTEGER),
        ],
        responses={200: GivePointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetPointSerializer
        return GivePointSerializer

class GivePointRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GivePointSerializer
    permission_classes = [IsAuthenticated]

class NewsListView(generics.ListAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer

class NewDetailView(generics.RetrieveAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer

class ResetAllStudentsPointsView(APIView):
    def post(self, request, *args, **kwargs):
        Student.objects.update(point=0)
        return Response({'message': 'All students\' points have been reset to 0.'}, status=status.HTTP_200_OK)


class MarkAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        news = get_object_or_404(New, id=pk)
        read_status, created = NewsReadStatus.objects.get_or_create(user=request.user, news=news)
        if not read_status.is_read:
            read_status.is_read = True
            read_status.save()

        serializer = NewsReadStatusSerializer(read_status)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllReadStatusAPIView(generics.ListAPIView):
    serializer_class = NewsReadStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NewsReadStatus.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate number of unread news items
        read_news_ids = queryset.values_list('news_id', flat=True)
        unread_news_ids = New.objects.exclude(id__in=read_news_ids).values_list('id', flat=True)
        total_news_count = New.objects.count()
        read_news_count = queryset.count()
        num_unread_news = total_news_count - read_news_count

        return Response({
            'num_unread_news': num_unread_news,
            'unread_news_ids': list(unread_news_ids),
            'read_news_ids': serializer.data
        })


class CourseAveragePointsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = Course.objects.all()
        result = []

        for course in courses:

            groups = Group.objects.filter(mentor__course=course)
            students = []
            for group in groups:
                students.extend(group.student_set.all())


            point_types = PointType.objects.all()

            course_avg_data = {}

            for point_type in point_types:

                give_points = GivePoint.objects.filter(student__in=students, point_type=point_type)
                avg_points = give_points.aggregate(Avg('amount'))['amount__avg']

                course_avg_data[point_type.name] = avg_points if avg_points is not None else 0

            result.append({
                course.name: course_avg_data
            })

        return Response(result, status=status.HTTP_200_OK)

class CourseAveragePointsListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):

        courses = Course.objects.all()
        course_avg_points = []

        for course in courses:
            students = Student.objects.filter(group__mentor__course=course)

            point_types = PointType.objects.all()
            point_type_avg_data = {}

            for point_type in point_types:

                give_points = GivePoint.objects.filter(student__in=students, point_type=point_type)
                avg_points = give_points.aggregate(Avg('amount'))['amount__avg']


                point_type_avg_data[point_type.name] = avg_points if avg_points is not None else 0


            course_avg_points.append({
                course.name: point_type_avg_data
            })

        return Response(course_avg_points)


