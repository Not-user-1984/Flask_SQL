from flask import Flask, jsonify, request, render_template
import psycopg2
import json
from utility import measure_time

app = Flask(__name__)

# Параметры подключения к базе данных
DB_HOST = 'localhost'
DB_NAME = 'demo'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'


def get_db_connection():
    """Функция для установления соединения с базой данных."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bookings', methods=['GET'])
@measure_time
def get_bookings():
    """Получение всех бронирований."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM bookings;
            """)
            bookings = cur.fetchall()
    return jsonify(bookings)


@app.route('/chesk', methods=['GET'])
@measure_time
def chesk():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT aircraft_code, fare_conditions, count(*)
                FROM seats
                GROUP BY aircraft_code, fare_conditions
                ORDER BY aircraft_code, fare_conditions
                LIMIT 100
            """)
            seats = cur.fetchall()
    return jsonify(seats)


@app.route('/bookings/<book_ref>', methods=['GET'])
@measure_time
def get_booking(book_ref):
    """Получение бронирования по book_ref."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM bookings WHERE book_ref = '{book_ref}';
            """)
            booking = cur.fetchone()
    return jsonify(booking) if booking else jsonify(
        {'message': 'Booking not found'}), 404


@app.route('/bookings', methods=['POST'])
@measure_time
def create_booking():
    """Создание нового бронирования."""
    data = request.json
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO bookings (book_ref, book_date, total_amount)
                VALUES ('{data['book_ref']}', '{data['book_date']}', {data['total_amount']})
                RETURNING *
            """)
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking), 201


@app.route('/bookings/<book_ref>', methods=['PUT'])
@measure_time
def update_booking(book_ref):
    """Обновление бронирования по book_ref."""
    data = request.json
    book_date = data.get('book_date')
    total_amount = data.get('total_amount')

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                UPDATE bookings
                SET book_date = '{book_date}', total_amount = {total_amount}
                WHERE book_ref = '{book_ref}'
                RETURNING *;
            """)
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking) if booking else jsonify(
        {'message': 'Booking not found'}), 404


@app.route('/bookings/<book_ref>', methods=['DELETE'])
@measure_time
def delete_booking(book_ref):
    """Удаление бронирования по book_ref."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                DELETE FROM bookings WHERE book_ref = '{book_ref}' RETURNING *;
            """)
            booking = cur.fetchone()
            conn.commit()
    return jsonify(booking) if booking else jsonify(
        {'message': 'Booking not found'}), 404


@app.route('/aircrafts', methods=['POST'])
@measure_time
def add_aircraft():
    data = request.json
    aircraft_code = data['aircraft_code']
    model = json.dumps(data['model'])
    range = data['range']

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO aircrafts_data (aircraft_code, model, range)
                VALUES ('{aircraft_code}', '{model}', {range})
            """)
            conn.commit()

    return jsonify({"message": "Aircraft added successfully"}), 201


@app.route('/flights', methods=['GET'])
@measure_time
def get_flights():
    """Получение информации о рейсах с INNER JOIN."""
    limit = request.args.get('limit', default=10, type=int)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    f.flight_id,
                    f.flight_no,
                    f.scheduled_departure,
                    f.scheduled_arrival,
                    dep.airport_name AS departure_airport,
                    arr.airport_name AS arrival_airport,
                    a.model AS aircraft_model
                FROM
                    Flights f
                INNER JOIN
                    Airports dep ON f.departure_airport = dep.airport_code
                INNER JOIN
                    Airports arr ON f.arrival_airport = arr.airport_code
                INNER JOIN
                    Aircrafts a ON f.aircraft_code = a.aircraft_code
                LIMIT {limit};
            """)
            flights = cur.fetchall()
    return jsonify(flights)


@app.route('/bookings_left', methods=['GET'])
@measure_time
def get_bookings_left():
    """Получение информации о бронированиях с LEFT JOIN."""
    limit = request.args.get('limit', default=10, type=int)
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    b.book_ref,
                    b.book_date,
                    b.total_amount,
                    t.ticket_no,
                    t.passenger_id,
                    t.passenger_name
                FROM
                    Bookings b
                LEFT JOIN
                    Tickets t ON b.book_ref = t.book_ref
                LIMIT {limit};
            """)
            bookings = cur.fetchall()
    return jsonify(bookings)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
