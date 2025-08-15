from flask import Flask, jsonify, request
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Date,
    Float,
    Integer,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.sql import func
from utility import measure_time

app = Flask(__name__)

# Параметры подключения к базе данных
DB_HOST = "localhost"
DB_NAME = "demo"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Создание подключения к базе данных через SQLAlchemy
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Модели
class Booking(Base):
    __tablename__ = "bookings"
    book_ref = Column(String, primary_key=True)
    book_date = Column(Date)
    total_amount = Column(Float)


class Seat(Base):
    __tablename__ = "seats"
    aircraft_code = Column(String, primary_key=True)
    seat_no = Column(String, primary_key=True)
    fare_conditions = Column(String)


class Flight(Base):
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String)
    scheduled_departure = Column(Date)
    scheduled_arrival = Column(Date)
    departure_airport = Column(String, ForeignKey("airports.airport_code"))
    arrival_airport = Column(String, ForeignKey("airports.airport_code"))
    aircraft_code = Column(String, ForeignKey("aircrafts_data.aircraft_code"))


class Airport(Base):
    __tablename__ = "airports"
    airport_code = Column(String, primary_key=True)
    airport_name = Column(JSON)


class Aircraft(Base):
    __tablename__ = "aircrafts_data"
    aircraft_code = Column(String, primary_key=True)
    model = Column(JSON)
    range = Column(Integer)


class Ticket(Base):
    __tablename__ = "tickets"
    ticket_no = Column(String, primary_key=True)
    book_ref = Column(String, ForeignKey("bookings.book_ref"))
    passenger_id = Column(String)
    passenger_name = Column(String)


@app.route("/bookings", methods=["GET"])
@measure_time
def get_bookings():
    """Получение всех бронирований."""
    session = Session()
    bookings = session.query(Booking).limit(100).all()
    session.close()
    return jsonify(
        [
            {
                "book_ref": booking.book_ref,
                "book_date": booking.book_date,
                "total_amount": booking.total_amount,
            }
            for booking in bookings
        ]
    )


@app.route("/chesk", methods=["GET"])
@measure_time
def chesk():
    """Получение статистики по местам в самолетах."""
    session = Session()
    seats = (
        session.query(
            Seat.aircraft_code, Seat.fare_conditions, func.count().label("count")
        )
        .group_by(Seat.aircraft_code, Seat.fare_conditions)
        .order_by(Seat.aircraft_code, Seat.fare_conditions)
        .limit(100)
        .all()
    )
    session.close()
    return jsonify(
        [
            {
                "aircraft_code": seat.aircraft_code,
                "fare_conditions": seat.fare_conditions,
                "count": seat.count,
            }
            for seat in seats
        ]
    )


@app.route("/bookings/<book_ref>", methods=["GET"])
@measure_time
def get_booking(book_ref):
    """Получение бронирования по book_ref."""
    session = Session()
    booking = session.query(Booking).filter_by(book_ref=book_ref).first()
    session.close()
    if booking:
        return jsonify(
            {
                "book_ref": booking.book_ref,
                "book_date": booking.book_date,
                "total_amount": booking.total_amount,
            }
        )
    return jsonify({"message": "Booking not found"}), 404


@app.route("/bookings", methods=["POST"])
@measure_time
def create_booking():
    """Создание нового бронирования."""
    data = request.json
    new_booking = Booking(
        book_ref=data.get("book_ref"),
        book_date=data.get("book_date"),
        total_amount=data.get("total_amount"),
    )
    session = Session()
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    session.close()
    return jsonify(
        {
            "book_ref": new_booking.book_ref,
            "book_date": new_booking.book_date,
            "total_amount": new_booking.total_amount,
        }
    ), 201


@app.route("/bookings/<book_ref>", methods=["PUT"])
@measure_time
def update_booking(book_ref):
    """Обновление бронирования по book_ref."""
    data = request.json
    session = Session()
    booking = session.query(Booking).filter_by(book_ref=book_ref).first()
    if booking:
        booking.book_date = data.get("book_date")
        booking.total_amount = data.get("total_amount")
        session.commit()
        session.refresh(booking)
    session.close()
    if booking:
        return jsonify(
            {
                "book_ref": booking.book_ref,
                "book_date": booking.book_date,
                "total_amount": booking.total_amount,
            }
        )
    return jsonify({"message": "Booking not found"}), 404


@app.route("/bookings/<book_ref>", methods=["DELETE"])
@measure_time
def delete_booking(book_ref):
    """Удаление бронирования по book_ref."""
    session = Session()
    booking = session.query(Booking).filter_by(book_ref=book_ref).first()
    if booking:
        session.delete(booking)
        session.commit()
    session.close()
    if booking:
        return jsonify(
            {
                "book_ref": booking.book_ref,
                "book_date": booking.book_date,
                "total_amount": booking.total_amount,
            }
        )
    return jsonify({"message": "Booking not found"}), 404


@app.route("/aircrafts", methods=["POST"])
@measure_time
def add_aircraft():
    """Добавление нового самолета."""
    data = request.json
    new_aircraft = Aircraft(
        aircraft_code=data.get("aircraft_code"),
        model=data.get("model"),
        range=data.get("range"),
    )
    session = Session()
    session.add(new_aircraft)
    session.commit()
    session.close()
    return jsonify({"message": "Aircraft added successfully"}), 201


@app.route("/flights", methods=["GET"])
@measure_time
def get_flights():
    """Получение информации о рейсах с INNER JOIN."""
    limit = request.args.get("limit", default=10, type=int)
    session = Session()

    # Создаем псевдонимы для таблицы Airport
    DepartureAirport = aliased(Airport, name="departure_airport")
    ArrivalAirport = aliased(Airport, name="arrival_airport")

    flights = (
        session.query(
            Flight.flight_id,
            Flight.flight_no,
            Flight.scheduled_departure,
            Flight.scheduled_arrival,
            DepartureAirport.airport_name.label("departure_airport"),
            ArrivalAirport.airport_name.label("arrival_airport"),
            Aircraft.model.label("aircraft_model"),
        )
        .join(
            DepartureAirport, Flight.departure_airport == DepartureAirport.airport_code
        )
        .join(ArrivalAirport, Flight.arrival_airport == ArrivalAirport.airport_code)
        .join(Aircraft, Flight.aircraft_code == Aircraft.aircraft_code)
        .limit(limit)
        .all()
    )
    session.close()
    return jsonify(
        [
            {
                "flight_id": flight.flight_id,
                "flight_no": flight.flight_no,
                "scheduled_departure": flight.scheduled_departure,
                "scheduled_arrival": flight.scheduled_arrival,
                "departure_airport": flight.departure_airport,
                "arrival_airport": flight.arrival_airport,
                "aircraft_model": flight.aircraft_model,
            }
            for flight in flights
        ]
    )


@app.route("/bookings_left", methods=["GET"])
@measure_time
def get_bookings_left():
    """Получение информации о бронированиях с LEFT JOIN."""
    limit = request.args.get("limit", default=10, type=int)
    session = Session()
    bookings = (
        session.query(
            Booking.book_ref,
            Booking.book_date,
            Booking.total_amount,
            Ticket.ticket_no,
            Ticket.passenger_id,
            Ticket.passenger_name,
        )
        .outerjoin(Ticket, Booking.book_ref == Ticket.book_ref)
        .limit(limit)
        .all()
    )
    session.close()
    return jsonify(
        [
            {
                "book_ref": booking.book_ref,
                "book_date": booking.book_date,
                "total_amount": booking.total_amount,
                "ticket_no": booking.ticket_no,
                "passenger_id": booking.passenger_id,
                "passenger_name": booking.passenger_name,
            }
            for booking in bookings
        ]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
