from model_bakery import baker

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from app.models import MeetingRoom, Employee, Reservation


class TestGetMeetingRooms(APITestCase):
    def setUp(cls) -> None:
        cls.meeting_room = baker.make(MeetingRoom)
        cls.booked_reservations = baker.make(Reservation, meeting_room=cls.meeting_room)

    def test_get_meeting_rooms(self):
        response = self.client.get(reverse("meeting-rooms-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.meeting_room.id))

    def test_get_meeting_room_reservation(self):
        employee = baker.make(Employee, username="admin", password="admin")

        self.client.force_authenticate(employee)

        response = self.client.get(
            reverse(
                "reservations-list", kwargs={"meeting_room_id": self.meeting_room.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data[0]["id"], str(self.booked_reservations.id))


class TestPostReservation(APITestCase):
    def setUp(cls) -> None:
        cls.meeting_room = baker.make(MeetingRoom, max_attendees=5, reservation=None)
        cls.booked_reservations = baker.make(
            Reservation,
            date_from="2023-10-30T11:00:00Z",
            date_to="2023-10-30T12:00:00Z",
            meeting_room=cls.meeting_room,
        )
        cls.employee = baker.make(Employee, username="admin", password="admin")
        cls.client.force_authenticate(cls.employee)

    def test_successful_reservation_creation(self):
        new_reservation = {
            "date_from": "2023-10-30T09:30:00Z",
            "date_to": "2023-10-30T10:00:00Z",
            "attendees_number": 1,
        }

        response = self.client.post(
            reverse(
                "reservations-list", kwargs={"meeting_room_id": self.meeting_room.id}
            ),
            new_reservation,
        )

        check_created_reservation_excistence = Reservation.objects.filter(
            date_from=new_reservation["date_from"], date_to=new_reservation["date_to"]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(check_created_reservation_excistence)

    def test_when_reserved_dates_choosen(self):
        new_reservation = {
            "date_from": "2023-10-30T10:15:00Z",
            "date_to": "2023-10-30T11:30:00Z",
            "attendees_number": 1,
        }

        response = self.client.post(
            reverse(
                "reservations-list", kwargs={"meeting_room_id": self.meeting_room.id}
            ),
            new_reservation,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            response.data["non_field_errors"][0], "Chosen dates are already reserved."
        )

    def test_when_reservation_with_over_max_attendees(self):
        new_reservation = {
            "date_from": "2023-10-30T09:30:00Z",
            "date_to": "2023-10-30T10:00:00Z",
            "attendees_number": 10,
        }

        response = self.client.post(
            reverse(
                "reservations-list", kwargs={"meeting_room_id": self.meeting_room.id}
            ),
            new_reservation,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            response.data["non_field_errors"][0],
            "There is not enough space for all attendees.",
        )


class TestDeleteReservation(APITestCase):
    def setUp(cls) -> None:
        cls.booked_reservations = baker.make(Reservation)
        cls.meeting_room = baker.make(MeetingRoom, reservation=cls.booked_reservations)
        cls.employee = baker.make(Employee, username="admin", password="admin")
        cls.client.force_authenticate(cls.employee)

    def test_successful_reservation_deletion(self):
        response = self.client.delete(
            reverse(
                "reservations-detail",
                kwargs={
                    "meeting_room_id": self.meeting_room.id,
                    "pk": self.booked_reservations.id,
                },
            )
        )

        check_deleted_reservation_excistence = Reservation.objects.filter(
            id=self.booked_reservations.id
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(check_deleted_reservation_excistence)
