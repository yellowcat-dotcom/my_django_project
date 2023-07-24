from django.utils import timezone
from rest_framework import serializers
from .models import *


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['id', 'address', 'working_hours', 'office_photo']  # что будем возвращать обратно клиенту


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'floor']

    # получается тут уже и валидаторы не нужны
    def validate_name(self, value):
        if Department.objects.filter(name=value).exists():
            raise serializers.ValidationError("Отдел с таким названием уже существует.")
        return value

    def validate_floor(self, value):
        if value < 0:
            raise serializers.ValidationError('Значение этажа не может быть отрицательным.')
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'photo', 'department']


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['id', 'number', 'floor', 'capacity', 'has_tv']


class CurrentUserDefault:
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user

    def __call__(self):
        return self.user


class ReservationSerializer(serializers.ModelSerializer):
    meeting_room = serializers.PrimaryKeyRelatedField(
        queryset=MeetingRoom.objects.all(),
        required=False
    )

    participants = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        many=True,
        required=False
    )

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time and end_time:
            if start_time > end_time:
                raise serializers.ValidationError('Время окончания раньше времени начала')
            if start_time < timezone.now():
                raise serializers.ValidationError('Время начала уже прошло')
        else:
            raise serializers.ValidationError('Необходимо указать и время начала, и время окончания')

        return attrs

    class Meta:
        model = Reservation
        fields = ['id', 'meeting_room', 'reserved_by', 'participants', 'start_time', 'end_time']



class ReservationForUserSerializer(serializers.ModelSerializer):
    participants = EmployeeSerializer(many=True)
    reserved_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Reservation
        fields = ['id', 'meeting_room', 'reserved_by', 'participants', 'start_time', 'end_time']
