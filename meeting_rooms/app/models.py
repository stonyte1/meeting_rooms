import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Employee(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = PhoneNumberField(blank=True, default="")
    reservations = models.ManyToManyField("MeetingRoom", through="Reservation")

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.username


class MeetingRoom(BaseModel):
    name = models.CharField(max_length=255)
    max_attendees = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    attendees_number = models.IntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ["-date_from", "-date_to"]

    def __str__(self):
        return f"{self.date_from}: {self.date_to}"
