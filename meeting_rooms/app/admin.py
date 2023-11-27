from django.contrib import admin

from app.models import Employee, MeetingRoom, Reservation


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "username",
        "is_staff",
        "password",
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]


admin.site.register(MeetingRoom)
admin.site.register(Reservation)
