from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utility import measure_time

app = Flask(__name__)

# Параметры подключения к базе данных
DB_HOST = 'localhost'
DB_NAME = 'demo'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Создание подключения к базе данных через SQLAlchemy
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    )
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Booking(Base):
    __tablename__ = 'bookings'
    book_ref = Column(String, primary_key=True)
    book_date = Column(Date)
    total_amount = Column(Float)


@app.route('/bookings', methods=['GET'])
@measure_time
def get_bookings():
    """Получение всех бронирований."""
    session = Session()
    bookings = session.query(Booking).all()
    session.close()
    return jsonify([{
        'book_ref': booking.book_ref,
        'book_date': booking.book_date,
        'total_amount': booking.total_amount
    } for booking in bookings])


@app.route('/bookings/<book_ref>', methods=['GET'])
@measure_time
def get_booking(book_ref):
    """Получение бронирования по book_ref."""
    session = Session()
    booking = session.query(Booking).filter_by(book_ref=book_ref).first()
    session.close()
    if booking:
        return jsonify({
            'book_ref': booking.book_ref,
            'book_date': booking.book_date,
            'total_amount': booking.total_amount
        })
    return jsonify({'message': 'Booking not found'}), 404


@app.route('/bookings', methods=['POST'])
@measure_time
def create_booking():
    """Создание нового бронирования."""
    data = request.json
    new_booking = Booking(
        book_ref=data.get('book_ref'),
        book_date=data.get('book_date'),
        total_amount=data.get('total_amount')
    )
    session = Session()
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    session.close()
    return jsonify({
        'book_ref': new_booking.book_ref,
        'book_date': new_booking.book_date,
        'total_amount': new_booking.total_amount
    }), 201


@app.route('/bookings/<book_ref>', methods=['PUT'])
@measure_time
def update_booking(book_ref):
    """Обновление бронирования по book_ref."""
    data = request.json
    session = Session()
    booking = session.query(Booking).filter_by(book_ref=book_ref).first()
    if booking:
        booking.book_date = data.get('book_date')
        booking.total_amount = data.get('total_amount')
        session.commit()
        session.refresh(booking)
    session.close()
    if booking:
        return jsonify({
            'book_ref': booking.book_ref,
            'book_date': booking.book_date,
            'total_amount': booking.total_amount
        })
    return jsonify({'message': 'Booking not found'}), 404


@app.route('/bookings/<book_ref>', methods=['DELETE'])
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
        return jsonify({
            'book_ref': booking.book_ref,
            'book_date': booking.book_date,
            'total_amount': booking.total_amount
        })
    return jsonify({'message': 'Booking not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
