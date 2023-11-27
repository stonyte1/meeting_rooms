from rest_framework import routers
from django.urls import path, include

from app.views import MeetingRoomViewSet, ReservationViewSet, EmployeeViewSet

router = routers.DefaultRouter()

router.register(r"meeting_rooms", MeetingRoomViewSet, basename="meeting-rooms")
router.register(r"employees", EmployeeViewSet, basename="employees")
router.register(
    r"meeting-rooms/(?P<meeting_room_id>[0-9a-f-]+)/reservations",
    ReservationViewSet,
    basename="reservations",
)

urlpatterns = [
    path("", include(router.urls)),
]
