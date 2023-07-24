from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsReadOnly
from .serializers import *
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# представления для Rest Framework

class ConfigurationAPIView(ListAPIView):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

    # нужно ли прописывать права доступа, если в данных представлениях есть только get запрос?
    permission_classes = [IsReadOnly]


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # нужно ли прописывать права доступа, если в данных представлениях есть только get запрос?
    permission_classes = [IsReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor']


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    # нужно ли прописывать права доступа, если в данных представлениях есть только get запрос?
    permission_classes = [IsReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']


class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer

    # нужно ли прописывать права доступа, если в данных представлениях есть только get запрос?
    permission_classes = [IsReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'capacity', 'has_tv']


class ReservationListAPIView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationCreateSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            employee = Employee.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
        serializer.save(reserved_by=employee)

    def post(self, request, format=None):
        # Получение объекта Employee на основе пользователя, связанного с токеном авторизации
        employee = request.user.employee

        # Передача объекта Employee в поле "reserved_by" при создании бронирования
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reserved_by=employee)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ReservationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CustomObtainAuthToken(ObtainAuthToken):
    # Пользовательский класс для получения токена с информацией о пользователе
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            employee = Employee.objects.create(user=user, first_name=user.first_name, last_name=user.last_name)
        return response
