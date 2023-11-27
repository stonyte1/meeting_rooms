from typing import Any
from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import MeetingRoom, Employee, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "date_from",
            "date_to",
            "attendees_number",
        ]

    def create(self, validated_data):
        validated_data["meeting_room_id"] = self.context["meeting_room_id"]
        validated_data["employee"] = self.context["employee_id"]
        return super().create(validated_data)

    def validate(self, attrs):
        if self.is_reserved(attrs["date_from"], attrs["date_to"]):
            raise ValidationError("Chosen dates are already reserved.")

        if not self.has_enough_space_for_attendees(attrs["attendees_number"]):
            raise ValidationError("There is not enough space for all attendees.")

        return super().validate(attrs)

    def is_reserved(self, date_from: datetime, date_to: datetime) -> bool:
        """Checks for date range overlap with existing reservations for an upcoming reservation."""
        check_are_available = Reservation.objects.filter(
            meeting_room=self.context["meeting_room_id"],
            date_from__lte=date_to,
            date_to__gte=date_from,
        )

        if check_are_available.exists():
            return True

        return False

    # docstring
    def has_enough_space_for_attendees(self, attendees_number: int):
        """Checks if upcoming attendees fit within the reserved room's capacity."""
        max_attendees = (
            MeetingRoom.objects.filter(id=self.context["meeting_room_id"])
            .first()
            .max_attendees
        )

        if max_attendees < attendees_number:
            return False

        return True


class MeetingRoomSerializer(serializers.ModelSerializer):
    reservations = serializers.SerializerMethodField()

    class Meta:
        model = MeetingRoom
        fields = ["id", "name", "max_attendees", "reservations"]

    def get_reservations(self, metting_room: MeetingRoom) -> Any:
        reservations = Reservation.objects.filter(meeting_room=metting_room)
        return ReservationSerializer(reservations, many=True).data


class EmployeeRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "reservations",
        ]
