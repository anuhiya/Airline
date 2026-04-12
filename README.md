# ✈ SkySearch — Airline Flight Web App

A simple Flask web application for browsing airline flights and seat availability, built for the Airline Flights and Booking database homework.

## Features

- **Search flights** by origin airport, destination airport, and a date range
- **Browse results** showing flight number, airline, route, departure date/time, duration, and aircraft type
- **View flight details** — click any flight to see capacity, booked seats, available seats, load factor, and the full passenger manifest

## Database Schema

```
Airport      (airport_code PK, name, city, country)
Aircraft     (plane_type PK, capacity)
FlightService(flight_number PK, airline_name, origin_code FK, dest_code FK, departure_time, duration)
Flight       (flight_number FK, departure_date, plane_type FK)   — PK: (flight_number, departure_date)
Passenger    (pid PK, passenger_name)
Booking      (pid FK, flight_number, departure_date, seat_number) — PK: (pid, flight_number, departure_date)
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize the SQLite database with sample data
python init_db.py

# 3. Run the Flask app
python app.py
```

Then open your browser to **http://localhost:5000**

## Sample Queries to Try

| Origin | Destination | Date Range |
|--------|------------|------------|
| JFK    | LAX        | 2025-04-10 to 2025-04-13 |
| JFK    | LHR        | 2025-04-10 to 2025-04-12 |
| JFK    | CDG        | 2025-04-10 to 2025-04-12 |
| LAX    | SFO        | 2025-04-10 to 2025-04-11 |

## Project Structure

```
airline_app/
├── app.py          # Flask routes and database queries
├── init_db.py      # Schema creation + sample data insertion
├── requirements.txt
└── templates/
    ├── base.html         # Shared layout, CSS
    ├── index.html        # Search form (Part a)
    ├── flights.html      # Flight results list (Part b)
    └── flight_detail.html # Seat availability detail (Part c)
```

## Notes

- Uses SQLite for simplicity, swap `DB_PATH` in `app.py` for PostgreSQL/MySQL as needed.
- All times are in GMT as specified.
- The app shows all flights regardless of whether they are fully booked.
