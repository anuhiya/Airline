from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "airline.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    airports = []
    conn = get_db()
    airports = conn.execute(
        "SELECT airport_code, name, city, country FROM Airport ORDER BY airport_code"
    ).fetchall()
    conn.close()

    if request.method == "POST":
        origin = request.form.get("origin", "").strip().upper()
        dest = request.form.get("dest", "").strip().upper()
        date_from = request.form.get("date_from", "")
        date_to = request.form.get("date_to", "")
        return redirect(
            url_for("flights", origin=origin, dest=dest,
                    date_from=date_from, date_to=date_to)
        )

    return render_template("index.html", airports=airports)


@app.route("/flights")
def flights():
    origin = request.args.get("origin", "").upper()
    dest = request.args.get("dest", "").upper()
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    conn = get_db()
    query = """
        SELECT
            f.flight_number,
            f.departure_date,
            fs.airline_name,
            fs.origin_code,
            fs.dest_code,
            fs.departure_time,
            fs.duration_mins,
            f.plane_type,
            ao.name  AS origin_name,
            ao.city  AS origin_city,
            ad.name  AS dest_name,
            ad.city  AS dest_city
        FROM Flight f
        JOIN FlightService fs ON f.flight_number = fs.flight_number
        JOIN Airport ao ON fs.origin_code = ao.airport_code
        JOIN Airport ad ON fs.dest_code   = ad.airport_code
        WHERE fs.origin_code = ?
          AND fs.dest_code   = ?
          AND f.departure_date BETWEEN ? AND ?
        ORDER BY f.departure_date, fs.departure_time
    """
    results = conn.execute(query, (origin, dest, date_from, date_to)).fetchall()
    conn.close()

    return render_template(
        "flights.html",
        flights=results,
        origin=origin,
        dest=dest,
        date_from=date_from,
        date_to=date_to,
    )


@app.route("/flight/<flight_number>/<departure_date>")
def flight_detail(flight_number, departure_date):
    conn = get_db()

    flight = conn.execute("""
        SELECT
            f.flight_number,
            f.departure_date,
            f.plane_type,
            fs.airline_name,
            fs.origin_code,
            fs.dest_code,
            fs.departure_time,
            fs.duration_mins,
            ac.capacity,
            ao.name  AS origin_name,
            ao.city  AS origin_city,
            ad.name  AS dest_name,
            ad.city  AS dest_city
        FROM Flight f
        JOIN FlightService fs ON f.flight_number = fs.flight_number
        JOIN Aircraft ac      ON f.plane_type    = ac.plane_type
        JOIN Airport ao       ON fs.origin_code  = ao.airport_code
        JOIN Airport ad       ON fs.dest_code    = ad.airport_code
        WHERE f.flight_number   = ?
          AND f.departure_date  = ?
    """, (flight_number, departure_date)).fetchone()

    bookings = conn.execute("""
        SELECT COUNT(*) AS booked_seats
        FROM Booking
        WHERE flight_number  = ?
          AND departure_date = ?
    """, (flight_number, departure_date)).fetchone()

    passengers = conn.execute("""
        SELECT p.passenger_name, b.seat_number
        FROM Booking b
        JOIN Passenger p ON b.pid = p.pid
        WHERE b.flight_number  = ?
          AND b.departure_date = ?
        ORDER BY b.seat_number
    """, (flight_number, departure_date)).fetchall()

    conn.close()

    if flight is None:
        return "Flight not found", 404

    booked = bookings["booked_seats"] if bookings else 0
    available = flight["capacity"] - booked

    return render_template(
        "flight_detail.html",
        flight=flight,
        booked=booked,
        available=available,
        passengers=passengers,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
