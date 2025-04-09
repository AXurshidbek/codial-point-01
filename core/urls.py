from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from auction.views import *
from main.views import *
# from main.schema import *

schema_view = get_schema_view(
    openapi.Info(
        title="Codial Gamification App's API",
        default_version='v1',
        description="Codial Gamification App's API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="otabekpm@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('users/get-me/', UserDetailView.as_view(), name='user-details'),
    path('courses/', CourseListCreateView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view()),
    path('groups/', GroupListCreateView.as_view(), name='groups'),
    path('groups/<int:pk>/', GroupRetrieveUpdateDestroyView.as_view()),
    path('mentors/', MentorListCreateView.as_view(), name='mentors'),
    path('mentors/<int:pk>/', MentorRetrieveUpdateDestroyView.as_view()),
    path('mentors/get-me/', MentorDetailView.as_view(), name='mentor-details'),
    path('students/', StudentListCreateView.as_view(), name='students'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view()),
    path('students/get-me/', StudentDetailView.as_view(), name='student-details'),
    path('point-types/', PointTypeListCreateView.as_view(), name='point_types'),
    path('point-types/<int:pk>/', PointTypeRetrieveUpdateDestroyView.as_view()),
    path('give-points/', GivePointListCreateView.as_view(), name='give_points'),
    path('give-points/<int:pk>/', GivePointRetrieveUpdateDestroyView.as_view()),
    path('auctions/',AuctionListView.as_view(),name='auction-list'),
    path('auction_create/',AuctionCreateView.as_view(),name='auction-create'),
    path('auctions/<int:pk>/',AuctionDetailView.as_view(),name='auction-detail'),
    path('current-auction/',CurrentAuctionDetailView.as_view(),name='current-auction-detail'),
    path('current-auction/products/',CurrentAuctionProductsView.as_view(),name='current-auction-products'),
    path('create-product/',CreateProductView.as_view(),name='create-product'),
    path('auctions/<int:pk>/products/',ProductListView.as_view(),name='product-list'),
    path('news/',NewsListView.as_view(),name='news-list'),
    path('news/<int:pk>/',NewDetailView.as_view(),name='news-detail'),
    path('news/<int:pk>/mark-as-read/', MarkAsReadAPIView.as_view(), name='mark_as_read'),
    # path('news/mark-as-read/', GetReadStatusAPIView.as_view(), name='mark_as_read_get'),
    path('news/get-read-status/', AllReadStatusAPIView.as_view(), name='get-read-status'),
    path('reset-points/',ResetAllStudentsPointsView.as_view(), name='reset-points'),
    path('average-points/',CourseAveragePointsListAPIView.as_view(), name='average-points'),
    # path('average-points-02/',CourseAveragePointsAPIView.as_view(), name='average-points'),
    # path('task/',include('second.urls'))
]

