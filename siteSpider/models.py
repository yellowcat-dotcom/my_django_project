from django.contrib.auth.models import User
from django.db import models
from solo.models import SingletonModel
from django.core.validators import MinValueValidator


class Department(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)  # Отчество (может быть пустым)
    photo = models.ImageField(upload_to='employee_photos/')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# новый класс для редактирования связи М2М
class MeetingParticipant(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class MeetingRoom(models.Model):
    number = models.CharField(max_length=10)
    floor = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    capacity = models.IntegerField()
    has_tv = models.BooleanField()

    def __str__(self):
        return self.number


class Reservation(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.SET_NULL, null=True)
    reserved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='reserved_rooms')
    participants = models.ManyToManyField(Employee, through=MeetingParticipant, blank=True,
                                          related_name='meeting_rooms')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)


class Configuration(SingletonModel):
    address = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=100)
    office_photo = models.ImageField(upload_to='office_photos/')

    def __str__(self):
        return self.address
