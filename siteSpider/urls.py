from django.urls import path, include
from drf_yasg import openapi
from .views import *
from rest_framework import routers
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'meeting-rooms', MeetingRoomViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title = 'Django',
        default_version='v1',
        description='Test discription',
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # маршруты для Rest Framework
    path('api/configuration/', ConfigurationAPIView.as_view(), name='configuration_api'),
    path('api/', include(router.urls)),
    path('api/reservations/', ReservationListAPIView.as_view(), name='reservations-list'),
    path('api/reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservations-detail'),

    # для токенов
    path('api/token/', CustomObtainAuthToken.as_view(), name='token_obtain_pair'),

    # Путь к документации Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
