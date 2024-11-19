# Flask_SQL

## Описание

Этот проект демонстрирует использование Flask для работы с базой данных PostgreSQL. В проекте используется демо-база данных, которую можно скачать по ссылке ниже.

## Установка и запуск

### 1. Скачайте демо-базу данных

Скачайте демо-базу данных по ссылке:

[https://postgrespro.ru/education/demodb](https://postgrespro.ru/education/demodb)

Поместите скачанный файл `demo.sql` в папку с проектом.

### 2. Установите Docker и Docker Compose

Убедитесь, что у вас установлены Docker и Docker Compose.

### 3. Запустите контейнеры

Запустите контейнеры с помощью Docker Compose:

```bash
docker-compose up -d
```

### 4. Накатите дамп базы данных

Выполните команду для загрузки дампа базы данных:

```bash
docker exec -i postgres_demo psql -U postgres -d demo < demo.sql
```

### 5. Подключитесь к базе данных

Подключитесь к базе данных в контейнере:

```bash
docker exec -it postgres_demo psql -U postgres -d demo
```

Проверьте наличие таблиц:

```sql
\dt
```

## Тестирование маршрутов

### Получение всех бронирований

```bash
curl http://localhost:5001/bookings
```

### Получение бронирования по `book_ref`

```bash
curl http://localhost:5000/bookings/<book_ref>
```

### Создание нового бронирования

```bash
curl -X POST -H "Content-Type: application/json" -d '{"book_ref": "123456", "book_date": "2023-11-12", "total_amount": 1000}' http://localhost:5001/bookings
```

### Обновление бронирования

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"book_date": "2023-11-13", "total_amount": 1200}' http://localhost:5000/bookings/123456
```

### Удаление бронирования

```bash
curl -X DELETE http://localhost:5000/bookings/123456
```

### Создание самолета

```bash
curl -X POST http://localhost:5001/aircrafts -H "Content-Type: application/json" -d '{
    "aircraft_code": "747",
    "model": {"en": "Boeing 747", "ru": "Боинг 747"},
    "range": 10000
}'
```

## Примеры SQL запросов

### Добавление мест в самолете

```sql
INSERT INTO seats VALUES ('123', '1A', 'Business');
```

### Группировка мест по самолетам и классам обслуживания

```sql
SELECT aircraft_code, fare_conditions, count(*) FROM seats
GROUP BY aircraft_code, fare_conditions
ORDER BY aircraft_code, fare_conditions LIMIT 100;
```

### Создание дополнительной таблицы

```sql
CREATE TABLE databases (
    is_open_source boolean,
    dbms_name text
);

INSERT INTO databases VALUES (TRUE, 'PostgreSQL');
INSERT INTO databases VALUES (FALSE, 'Oracle');
INSERT INTO databases VALUES (TRUE, 'MySQL');
INSERT INTO databases VALUES (FALSE, 'MS SQL Server');
```


Для демонстрации работы различных типов JOIN (LEFT JOIN, RIGHT JOIN, INNER JOIN) на практике, можно составить несколько запросов к базе данных, описанной в диаграмме схемы данных. Вот несколько примеров:

### 1. INNER JOIN (Центральный JOIN)
**Задача:** Получить информацию о рейсах, включая данные о самолетах и аэропортах отправления и прибытия.

```sql
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
    Aircrafts a ON f.aircraft_code = a.aircraft_code;
```

### 2. LEFT JOIN
**Задача:** Получить информацию о всех бронированиях, включая данные о билетах, даже если билеты не были оформлены.

```sql
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
    Tickets t ON b.book_ref = t.book_ref;
```

### 3. RIGHT JOIN
**Задача:** Получить информацию о всех билетах, включая данные о бронированиях, даже если бронирования не были сделаны.

```sql
SELECT 
    t.ticket_no, 
    t.passenger_id, 
    t.passenger_name, 
    b.book_ref, 
    b.book_date, 
    b.total_amount
FROM 
    Bookings b
RIGHT JOIN 
    Tickets t ON b.book_ref = t.book_ref;
```

### 4. LEFT JOIN с условием
**Задача:** Получить информацию о всех рейсах, включая данные о посадочных талонах, даже если посадочные талоны не были выданы.

```sql
SELECT 
    f.flight_id, 
    f.flight_no, 
    f.scheduled_departure, 
    f.scheduled_arrival, 
    bp.boarding_no, 
    bp.seat_no
FROM 
    Flights f
LEFT JOIN 
    Boarding_passes bp ON f.flight_id = bp.flight_id;
```

### 5. RIGHT JOIN с условием
**Задача:** Получить информацию о всех посадочных талонах, включая данные о рейсах, даже если рейсы не были назначены.

```sql
SELECT 
    bp.boarding_no, 
    bp.seat_no, 
    f.flight_id, 
    f.flight_no, 
    f.scheduled_departure, 
    f.scheduled_arrival
FROM 
    Flights f
RIGHT JOIN 
    Boarding_passes bp ON f.flight_id = bp.flight_id;
```

### 6. INNER JOIN с условием
**Задача:** Получить информацию о всех билетах, включая данные о перелетах, только если перелеты были оформлены.

```sql
SELECT 
    t.ticket_no, 
    t.passenger_id, 
    t.passenger_name, 
    tf.flight_id, 
    tf.fare_conditions, 
    tf.amount
FROM 
    Tickets t
INNER JOIN 
    Ticket_flights tf ON t.ticket_no = tf.ticket_no;
```

Эти запросы демонстрируют различные типы JOIN и их применение в реальных сценариях работы с базой данных.