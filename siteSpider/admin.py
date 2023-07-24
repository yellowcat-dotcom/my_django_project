from django.contrib import admin
from .models import *


class MeetingParticipantInline(admin.TabularInline):
    model = MeetingParticipant


class ReservationAdmin(admin.ModelAdmin):
    inlines = [MeetingParticipantInline]


admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(MeetingRoom)
admin.site.register(Configuration)
admin.site.register(Reservation,ReservationAdmin)
