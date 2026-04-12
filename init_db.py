"""
init_db.py:
Populates airline.db with the exact schema and data from the homework SQL file.
PostgreSQL INTERVAL durations are stored as integer minutes for SQLite compatibility.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "airline.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS Booking;
        DROP TABLE IF EXISTS Flight;
        DROP TABLE IF EXISTS FlightService;
        DROP TABLE IF EXISTS Aircraft;
        DROP TABLE IF EXISTS Airport;
        DROP TABLE IF EXISTS Passenger;

        CREATE TABLE Airport (
            airport_code VARCHAR(3) PRIMARY KEY,
            name         VARCHAR(100) NOT NULL,
            city         VARCHAR(50)  NOT NULL,
            country      VARCHAR(50)  NOT NULL
        );

        CREATE TABLE Aircraft (
            plane_type VARCHAR(30) PRIMARY KEY,
            capacity   INT NOT NULL
        );

        CREATE TABLE FlightService (
            flight_number  VARCHAR(10) PRIMARY KEY,
            airline_name   VARCHAR(50)  NOT NULL,
            origin_code    VARCHAR(3)   NOT NULL REFERENCES Airport(airport_code),
            dest_code      VARCHAR(3)   NOT NULL REFERENCES Airport(airport_code),
            departure_time VARCHAR(8)   NOT NULL,
            duration_mins  INTEGER      NOT NULL
        );

        CREATE TABLE Flight (
            flight_number  VARCHAR(10) NOT NULL REFERENCES FlightService(flight_number),
            departure_date DATE        NOT NULL,
            plane_type     VARCHAR(30) NOT NULL REFERENCES Aircraft(plane_type),
            PRIMARY KEY (flight_number, departure_date)
        );

        CREATE TABLE Passenger (
            pid            INT PRIMARY KEY,
            passenger_name VARCHAR(100) NOT NULL
        );

        CREATE TABLE Booking (
            pid            INT         NOT NULL REFERENCES Passenger(pid),
            flight_number  VARCHAR(10) NOT NULL,
            departure_date DATE        NOT NULL,
            seat_number    INT         NOT NULL,
            PRIMARY KEY (pid, flight_number, departure_date),
            FOREIGN KEY (flight_number, departure_date) REFERENCES Flight(flight_number, departure_date)
        );
    """)

    airports = [
        ("JFK","John F Kennedy International","New York","United States"),
        ("LAX","Los Angeles International","Los Angeles","United States"),
        ("ORD","O'Hare International","Chicago","United States"),
        ("MDW","Midway International","Chicago","United States"),
        ("LHR","Heathrow Airport","London","United Kingdom"),
        ("CDG","Charles de Gaulle Airport","Paris","France"),
        ("ORY","Paris Orly Airport","Paris","France"),
        ("SFO","San Francisco International","San Francisco","United States"),
        ("MIA","Miami International","Miami","United States"),
        ("ATL","Hartsfield-Jackson International","Atlanta","United States"),
        ("NRT","Narita International","Tokyo","Japan"),
        ("SIN","Changi Airport","Singapore","Singapore"),
    ]

    aircraft = [
        ("CRJ-200",10),
        ("Boeing 737",20),
        ("Airbus A320",15),
        ("Boeing 787",25),
    ]

    # duration_mins: INTERVAL '3 hours 30 minutes'=210, '6 hours'=360, etc.
    flight_services = [
        ("AA101","American Airlines","JFK","LAX","08:00:00",210),
        ("AA205","American Airlines","JFK","LAX","14:00:00",210),
        ("UA302","United Airlines","SFO","ORD","09:00:00",360),
        ("DL410","Delta Air Lines","ATL","MIA","10:00:00",150),
        ("BA178","British Airways","LHR","JFK","10:00:00",180),
        ("AF023","Air France","CDG","NRT","22:00:00",1140),
        ("SQ321","Singapore Airlines","SIN","LHR","23:00:00",420),
        ("AA550","American Airlines","ORD","MIA","07:00:00",240),
        ("DL620","Delta Air Lines","JFK","ATL","16:00:00",150),
        ("UA789","United Airlines","LAX","SFO","12:00:00",90),
    ]

    flights = [
        ("AA101","2025-12-29","Boeing 737"),
        ("AA101","2025-12-31","Boeing 737"),
        ("AA205","2025-12-31","Boeing 737"),
        ("UA302","2025-12-31","CRJ-200"),
        ("DL410","2025-12-31","Airbus A320"),
        ("BA178","2025-12-31","Boeing 787"),
        ("AF023","2025-12-30","Boeing 787"),
        ("SQ321","2025-12-30","Boeing 787"),
        ("DL620","2025-12-30","Airbus A320"),
        ("DL620","2025-12-31","Airbus A320"),
        ("AA550","2025-12-31","CRJ-200"),
        ("UA789","2025-12-31","Airbus A320"),
    ]

    passengers = [
        (1,"John Adams"),(2,"Sarah Miller"),(3,"Michael Chen"),(4,"Emily Wong"),
        (5,"David Park"),(6,"Lisa Johnson"),(7,"James Brown"),(8,"Maria Garcia"),
        (9,"Robert Kim"),(10,"Jennifer Lee"),(11,"Thomas Wilson"),(12,"Amanda Clark"),
        (13,"Christopher Davis"),(14,"Jessica Martinez"),(15,"Daniel Taylor"),
        (16,"Rachel Anderson"),(17,"William Thomas"),(18,"Nicole White"),
        (19,"Kevin Harris"),(20,"Stephanie Moore"),(21,"Andrew Jackson"),
        (22,"Michelle Robinson"),(23,"Brian Lewis"),(24,"Laura Walker"),(25,"Steven Hall"),
    ]

    bookings = [
        # AA101 / 2025-12-29  (Boeing 737, cap 20) → 5 booked
        (1,"AA101","2025-12-29",1),(2,"AA101","2025-12-29",2),(3,"AA101","2025-12-29",3),
        (4,"AA101","2025-12-29",4),(5,"AA101","2025-12-29",5),
        # AA101 / 2025-12-31  (Boeing 737, cap 20) → 15 booked
        (1,"AA101","2025-12-31",1),(2,"AA101","2025-12-31",2),(3,"AA101","2025-12-31",3),
        (4,"AA101","2025-12-31",4),(5,"AA101","2025-12-31",5),(6,"AA101","2025-12-31",6),
        (7,"AA101","2025-12-31",7),(8,"AA101","2025-12-31",8),(9,"AA101","2025-12-31",9),
        (10,"AA101","2025-12-31",10),(11,"AA101","2025-12-31",11),(12,"AA101","2025-12-31",12),
        (13,"AA101","2025-12-31",13),(14,"AA101","2025-12-31",14),(15,"AA101","2025-12-31",15),
        # AA205 / 2025-12-31  (Boeing 737, cap 20) → 4 booked
        (16,"AA205","2025-12-31",1),(17,"AA205","2025-12-31",2),
        (18,"AA205","2025-12-31",3),(19,"AA205","2025-12-31",4),
        # UA302 / 2025-12-31  (CRJ-200, cap 10) → 10 booked FULL
        (1,"UA302","2025-12-31",1),(2,"UA302","2025-12-31",2),(3,"UA302","2025-12-31",3),
        (4,"UA302","2025-12-31",4),(5,"UA302","2025-12-31",5),(6,"UA302","2025-12-31",6),
        (7,"UA302","2025-12-31",7),(8,"UA302","2025-12-31",8),(9,"UA302","2025-12-31",9),
        (10,"UA302","2025-12-31",10),
        # DL410 / 2025-12-31  (Airbus A320, cap 15) → 14 booked
        (5,"DL410","2025-12-31",1),(6,"DL410","2025-12-31",2),(7,"DL410","2025-12-31",3),
        (8,"DL410","2025-12-31",4),(9,"DL410","2025-12-31",5),(10,"DL410","2025-12-31",6),
        (11,"DL410","2025-12-31",7),(12,"DL410","2025-12-31",8),(13,"DL410","2025-12-31",9),
        (14,"DL410","2025-12-31",10),(15,"DL410","2025-12-31",11),(16,"DL410","2025-12-31",12),
        (17,"DL410","2025-12-31",13),(18,"DL410","2025-12-31",14),
        # BA178 / 2025-12-31  (Boeing 787, cap 25) → 6 booked
        (20,"BA178","2025-12-31",1),(21,"BA178","2025-12-31",2),(22,"BA178","2025-12-31",3),
        (23,"BA178","2025-12-31",4),(24,"BA178","2025-12-31",5),(25,"BA178","2025-12-31",6),
        # AF023 / 2025-12-30  (Boeing 787, cap 25) → 4 booked
        (1,"AF023","2025-12-30",1),(2,"AF023","2025-12-30",2),
        (3,"AF023","2025-12-30",3),(4,"AF023","2025-12-30",4),
        # SQ321 / 2025-12-30  (Boeing 787, cap 25) → 3 booked
        (5,"SQ321","2025-12-30",1),(6,"SQ321","2025-12-30",2),(7,"SQ321","2025-12-30",3),
        # DL620 / 2025-12-30  (Airbus A320, cap 15) → 4 booked
        (10,"DL620","2025-12-30",1),(11,"DL620","2025-12-30",2),
        (12,"DL620","2025-12-30",3),(13,"DL620","2025-12-30",4),
        # DL620 / 2025-12-31  (Airbus A320, cap 15) → 5 booked
        (20,"DL620","2025-12-31",1),(21,"DL620","2025-12-31",2),(22,"DL620","2025-12-31",3),
        (23,"DL620","2025-12-31",4),(24,"DL620","2025-12-31",5),
        # AA550 / 2025-12-31  (CRJ-200, cap 10) → 7 booked
        (8,"AA550","2025-12-31",1),(9,"AA550","2025-12-31",2),(10,"AA550","2025-12-31",3),
        (11,"AA550","2025-12-31",4),(12,"AA550","2025-12-31",5),(13,"AA550","2025-12-31",6),
        (14,"AA550","2025-12-31",7),
        # UA789 / 2025-12-31  (Airbus A320, cap 15) → 3 booked
        (22,"UA789","2025-12-31",1),(23,"UA789","2025-12-31",2),(24,"UA789","2025-12-31",3),
    ]

    cur.executemany("INSERT INTO Airport VALUES (?,?,?,?)", airports)
    cur.executemany("INSERT INTO Aircraft VALUES (?,?)", aircraft)
    cur.executemany("INSERT INTO FlightService VALUES (?,?,?,?,?,?)", flight_services)
    cur.executemany("INSERT INTO Flight VALUES (?,?,?)", flights)
    cur.executemany("INSERT INTO Passenger VALUES (?,?)", passengers)
    cur.executemany("INSERT INTO Booking VALUES (?,?,?,?)", bookings)

    conn.commit()
    conn.close()
    print("airline.db initialised with CS 6083 Spring 2026 homework data.")


if __name__ == "__main__":
    init_db()
