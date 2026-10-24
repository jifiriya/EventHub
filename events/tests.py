
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Event, Reservation


class EventHubAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.event = Event.objects.create(
            title='Django Conference',
            venue='Bangalore Convention Centre',
            date='2027-09-20',
            total_seats=5,
            available_seats=5,
            status='upcoming'
        )

    def test_create_event(self):
        response = self.client.post(
            '/api/events/',
            {
                'title': 'Python Meetup',
                'venue': 'Kochi',
                'date': '2027-10-15',
                'total_seats': 100,
                'available_seats': 100,
                'status': 'upcoming',
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

    def test_list_events(self):
        response = self.client.get('/api/events/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_events_by_status(self):
        response = self.client.get(
            '/api/events/?status=upcoming'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_events_by_venue(self):
        response = self.client.get(
            '/api/events/?venue=bangalore'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_available_seats_validation(self):
        response = self.client.post(
            '/api/events/',
            {
                'title': 'Invalid Event',
                'venue': 'Kochi',
                'date': '2027-10-15',
                'total_seats': 10,
                'available_seats': 20,
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_create_reservation(self):
        response = self.client.post(
            '/api/reservations/',
            {
                'event': self.event.id,
                'attendee_name': 'Priya Sharma',
                'attendee_email': 'priya@example.com',
                'seats_reserved': 2,
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 3)

        self.assertEqual(
            Reservation.objects.count(), 1
        )

    def test_overbooking(self):
        response = self.client.post(
            '/api/reservations/',
            {
                'event': self.event.id,
                'attendee_name': 'Rahul',
                'attendee_email': 'rahul@example.com',
                'seats_reserved': 10,
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)

        self.event.refresh_from_db()
        self.assertEqual(self.event.available_seats, 5)

    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(
            event=self.event,
            attendee_name='Priya Sharma',
            attendee_email='priya@example.com',
            seats_reserved=2
        )

        self.event.available_seats = 3
        self.event.save()

        response = self.client.post(
            f'/api/reservations/{reservation.id}/cancel/'
        )

        self.assertEqual(response.status_code, 200)

        self.event.refresh_from_db()
        reservation.refresh_from_db()

        self.assertEqual(self.event.available_seats, 5)
        self.assertEqual(reservation.status, 'cancelled')

    def test_double_cancellation(self):
        reservation = Reservation.objects.create(
            event=self.event,
            attendee_name='Priya',
            attendee_email='priya@example.com',
            seats_reserved=2,
            status='cancelled'
        )

        response = self.client.post(
            f'/api/reservations/{reservation.id}/cancel/'
        )

        self.assertEqual(response.status_code, 400)

    def test_filter_reservations_by_event(self):
        Reservation.objects.create(
            event=self.event,
            attendee_name='Priya',
            attendee_email='priya@example.com',
            seats_reserved=1
        )

        response = self.client.get(
            f'/api/reservations/?event_id={self.event.id}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_reservations_count(self):
        Reservation.objects.create(
            event=self.event,
            attendee_name='Priya',
            attendee_email='priya@example.com',
            seats_reserved=1
        )

        response = self.client.get(
            f'/api/events/{self.event.id}/'
        )

        self.assertEqual(
            response.data['reservations_count'], 1
        )

