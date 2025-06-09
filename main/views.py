from datetime import datetime
from tokenize import group

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce

from django.db.models import Avg, FloatField

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
    ordering_fields = ['id', 'user__username', 'birth_date', 'created_at','point','group','group__mentor' ,'-point','created_at' ]
    search_fields = ['user__username','user__first_name','user__last_name', 'bio']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset', openapi.IN_QUERY,
                              description="The initial index to start returning results from",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Tartiblash mezoni (masalan: user__username, group , birth_date , group__mentor, group, -point, 'point)",
                type=openapi.TYPE_STRING,
                format='string'
            ),
            openapi.Parameter(
                'filtering',
                openapi.IN_QUERY,
                description="Filterlash mezoni (masalan: group__mentor=1, group=2, point_type=3,student__group=4)",
                type=openapi.TYPE_STRING,
                format='integer'
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Qidirish so'zi (ism yoki bio bo'yicha) (masalan: 'Azizbek')",
                type=openapi.TYPE_STRING,
                format='string'
            )
        ],
        responses={200: GivePointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
    ordering_fields = ['id', 'amount','-amount', 'date','-date', 'created_at', 'student__point']
    search_fields = ['description']
    pagination_class=CustomLimitOffsetPagination


    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return", type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset', openapi.IN_QUERY, description="The initial index to start returning results from", type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Boshlanish sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Tartiblash mezoni (masalan: -date, date, -amount,amount, student__point)",
                type=openapi.TYPE_STRING,
                format='string'
            ),
            openapi.Parameter(
                'filtering',
                openapi.IN_QUERY,
                description="Filterlash mezoni (masalan: mentor=1, student=2, point_type=3,student__group=4)",
                type=openapi.TYPE_STRING,
                format='integer'
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Qidirish so'zi (description bo'yicha) (masalan: 'homework', 'exam')",
                type=openapi.TYPE_STRING,
                format='string'
            )
        ],
        responses={200: GivePointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetPointSerializer
        return GivePointSerializer


class GivenPointListView(generics.ListAPIView):
    queryset = GivePoint.objects.all()
    serializer_class = GetPointSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['mentor', 'student', 'point_type', 'date', 'student__group']
    ordering_fields = ['id', 'amount', 'date', 'created_at']
    search_fields = ['description']
    pagination_class = CustomLimitOffsetPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return", type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset', openapi.IN_QUERY, description="The initial index to start returning results from", type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'date_from',
                openapi.IN_QUERY,
                description="Boshlanish sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'date_to',
                openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            )
        ],
        responses={200: GivePointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Umumiy o'rtacha ball
        average_amount = queryset.aggregate(
            average=Coalesce(Avg('amount'), 0, output_field=FloatField())
        )['average']

        # Umumiy miqdor (foizlar uchun)
        total_amount = queryset.aggregate(
            total=Coalesce(Sum('amount'), 0, output_field=FloatField())
        )['total']

        # Point type bo'yicha o'rtacha ball va foiz
        point_type_stats = (
            queryset.values('point_type__name')
            .annotate(
                amount_avg=Coalesce(Avg('amount'), 0, output_field=FloatField()),
                amount_sum=Coalesce(Sum('amount'), 0, output_field=FloatField())
            )
            .annotate(
                percentage=Coalesce(
                    (100.0 * Sum('amount') / total_amount if total_amount else 0),
                    0,
                    output_field=FloatField()
                )
            )
            .order_by('point_type__name')
        )

        # Vaqt oralig'i
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        return Response({
            'average_amount': average_amount,
            'point_type_stats': list(point_type_stats),
            'date_from': date_from,
            'date_to': date_to
        })

# class StudentPointsListView(generics.ListAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_fields = ['user__username', 'group', 'birth_date', 'group__mentor']
#     ordering_fields = ['id', 'user__username', 'birth_date', 'created_at', 'point', 'group', 'group__mentor']
#     search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
#     pagination_class = CustomLimitOffsetPagination
#
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return",
#                               type=openapi.TYPE_INTEGER),
#             openapi.Parameter('offset', openapi.IN_QUERY,
#                               description="The initial index to start returning results from",
#                               type=openapi.TYPE_INTEGER),
#             openapi.Parameter(
#                 'date_from',
#                 openapi.IN_QUERY,
#                 description="Boshlanish sanasi (YYYY-MM-DD formatida)",
#                 type=openapi.TYPE_STRING,
#                 format='date'
#             ),
#             openapi.Parameter(
#                 'date_to',
#                 openapi.IN_QUERY,
#                 description="Tugash sanasi (YYYY-MM-DD formatida)",
#                 type=openapi.TYPE_STRING,
#                 format='date'
#             )
#         ],
#         responses={200: GivePointSerializer(many=True)}
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         # queryset = queryset.filter(group=37)
#         return queryset
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         # queryset=queryset.filter(group__mentor__user=request.user)
#         start_date = request.query_params.get('start_date')
#         end_date = request.query_params.get('end_date')
#
#         serializer = self.get_serializer(queryset, many=True)
#         data = serializer.data
#
#         stats_map = {}
#         for student in queryset:
#             givepoints = GivePoint.objects.filter(student=student)
#             if start_date:
#                 givepoints = givepoints.filter(date__gte=start_date)
#             if end_date:
#                 givepoints = givepoints.filter(date__lte=end_date)
#
#             total_points = givepoints.aggregate(
#                 total=Coalesce(Sum('amount'), 0)
#             )['total']
#
#             give_point_count = givepoints.aggregate(
#                 count=Count('id')
#             )['count']
#
#             point_type_stats = (
#                 givepoints
#                 .values('point_type__name')
#                 .annotate(
#                     avg=Avg('amount'),
#                     count=Count('id'),
#                     sum=Sum('amount')
#                 )
#             )
#
#             total_sum = sum(item['sum'] for item in point_type_stats) or 1
#
#             point_type_combined = []
#             for item in point_type_stats:
#                 percentage = round((item['sum'] / total_sum) * 100, 2)
#                 point_type_combined.append({
#                     'point_type__name': item['point_type__name'],
#                     'total': item['sum'],
#                     'avg': item['avg'],
#                     'percentage': percentage,
#                     'count': item['count']
#                 })
#
#             stats_map[student.id] = {
#                 'total_points': total_points,
#                 'give_point_count': give_point_count,
#                 'point_type': point_type_combined
#             }
#
#         for item in data:
#             student_id = item['id']
#             stats = stats_map.get(student_id, {})
#             item.update({
#                 'total_points': stats.get('total_points', 0),
#                 'give_point_count': stats.get('give_point_count', 0),
#                 'point_type': stats.get('point_type', [])
#             })
#
#         return Response(data)


class StudentPointsListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['user__username', 'group', 'birth_date', 'group__mentor']
    ordering_fields = ['id', 'user__username', 'birth_date', 'created_at', 'point', 'group', 'group__mentor']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    pagination_class = CustomLimitOffsetPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('limit', openapi.IN_QUERY, description="How many results to return",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('offset', openapi.IN_QUERY,
                              description="The initial index to start returning results from",
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Boshlanish sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD formatida)",
                type=openapi.TYPE_STRING,
                format='date'
            )
        ],
        responses={200: GivePointSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        queryset = super().get_queryset()
        user = self.request.user
        if hasattr(user, 'mentor'):
            queryset = queryset.filter(group__mentor=user.mentor)
            return queryset
        return queryset.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        from datetime import datetime

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = None

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                end_date = None

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        stats_map = {}
        for student in queryset:
            givepoints = GivePoint.objects.filter(student=student)
            if start_date:
                givepoints = givepoints.filter(date__gte=start_date)
            if end_date:
                givepoints = givepoints.filter(date__lte=end_date)

            total_points = givepoints.aggregate(
                total=Coalesce(Sum('amount'), 0)
            )['total']

            give_point_count = givepoints.aggregate(
                count=Count('id')
            )['count']

            point_type_stats = (
                givepoints
                .values('point_type__name')
                .annotate(
                    avg=Avg('amount'),
                    count=Count('id'),
                    sum=Sum('amount')
                )
            )

            total_sum = sum(item['sum'] for item in point_type_stats) or 1

            point_type_combined = []
            for item in point_type_stats:
                percentage = round((item['sum'] / total_sum) * 100, 2)
                point_type_combined.append({
                    'point_type__name': item['point_type__name'],
                    'total': item['sum'],
                    'avg': item['avg'],
                    'percentage': percentage,
                    'count': item['count']
                })

            stats_map[student.id] = {
                'total_points': total_points,
                'give_point_count': give_point_count,
                'point_type': point_type_combined
            }

        total_items = queryset.count()
        for item in data:
            student_id = item['id']
            stats = stats_map.get(student_id, {})
            item.update({
                'total_points': stats.get('total_points', 0),
                'give_point_count': stats.get('give_point_count', 0),
                'point_type': stats.get('point_type', [])
            })

        response_data = {
            'total_items': total_items,
            'start_date': start_date,
            'end_date': end_date,
            'results': data
        }

        return Response(response_data)


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


