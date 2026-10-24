# EventHub


EventHub is a backend REST API developed using Django
and Django REST Framework.

The application allows users to browse events, reserve
seats, and cancel reservations.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Django ORM

## Features

- Create, view, update, and delete events
- Filter events by status and venue
- Reserve seats for upcoming and ongoing events
- Validate available seats before reservation
- Prevent ordinary overbooking requests
- Cancel reservations and restore seats
- Filter reservations by event ID
- Log HTTP requests using custom middleware

## Installation

Clone the repository:

git clone https://github.com/jifiriya/EventHub.git

cd eventhub

Create a virtual environment:

python3 -m venv venv

Activate the environment:

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run migrations:

python manage.py migrate

Start the server:

python manage.py runserver

API Base URL:

http://127.0.0.1:8000/api/

## Event Endpoints

GET /api/events/
List all events.

POST /api/events/
Create a new event.

GET /api/events/{id}/
Retrieve an event.

PUT /api/events/{id}/
Update an event.

PATCH /api/events/{id}/
Partially update an event.

DELETE /api/events/{id}/
Delete an event.

GET /api/events/?status=upcoming
Filter events by status.

GET /api/events/?venue=Bangalore
Filter events by venue.

## Reservation Endpoints

GET /api/reservations/
List reservations.

POST /api/reservations/
Create a reservation.

GET /api/reservations/{id}/
Retrieve a reservation.

PUT /api/reservations/{id}/
Update a reservation.

PATCH /api/reservations/{id}/
Partially update a reservation.

DELETE /api/reservations/{id}/
Delete a reservation.

GET /api/reservations/?event_id=1
Filter reservations by event.

POST /api/reservations/{id}/cancel/
Cancel a reservation and restore its seats.

## Sample Event Request

POST /api/events/

{
  "title": "PyCon India 2027",
  "venue": "Bangalore",
  "date": "2027-09-20",
  "total_seats": 500,
  "available_seats": 500,
  "status": "upcoming"
}

## Sample Reservation Request

POST /api/reservations/

{
  "event": 1,
  "attendee_name": "Priya Sharma",
  "attendee_email": "priya@example.com",
  "seats_reserved": 2
}

## Design Decision

Seat availability is validated using DRF serializers.

When a reservation is created, the number of reserved
seats is deducted from the event's available_seats
field in the serializer's create() method.

This keeps reservation creation and seat deduction
logic together and makes the implementation easy
to understand and maintain.


## Middleware

RequestLoggingMiddleware records:

- HTTP method
- Request URL
- HTTP response status
- Request processing duration


## Running Tests

python manage.py test events

