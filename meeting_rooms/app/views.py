from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError

from app.models import MeetingRoom, Employee, Reservation
from app.serializer import (
    MeetingRoomSerializer,
    ReservationSerializer,
    EmployeeRoomSerializer,
)


class MeetingRoomViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class EmployeeViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Employee.objects.all()
    serializer_class = EmployeeRoomSerializer


class ReservationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_serializer_context(self) -> dict[str, str]:
        if self.request.user.is_authenticated:
            context = {
                "employee_id": self.request.user,
                "meeting_room_id": self.kwargs["meeting_room_id"],
            }
        else:
            raise ValidationError("Unregonized user")
        return context
