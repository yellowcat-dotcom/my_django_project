import django_filters
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Employee, MeetingRoom, Department


class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.CharFilter(field_name='department__name', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['department']


class MeetingRoomFilterSet(FilterSet):
    department = ModelChoiceFilter(field_name='reserved_by__department', queryset=Department.objects.all())

    class Meta:
        model = MeetingRoom
        fields = ['department']