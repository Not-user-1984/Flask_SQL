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


### Тестовые данные для Postman

#### 1. GET /bookings
- **Описание**: Получение всех бронирований.
- **Метод**: GET
- **URL**: `http://0.0.0.0:5002/bookings`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  [
    {
      "book_ref": "ABC123",
      "book_date": "2025-01-01",
      "total_amount": 150.50
    },
    {
      "book_ref": "DEF456",
      "book_date": "2025-02-01",
      "total_amount": 200.75
    }
  ]
  ```
- **Пояснение**: Возвращает список всех записей из таблицы `bookings`. Если таблица пуста, вернется пустой массив `[]`.

#### 2. GET /bookings/<book_ref>
- **Описание**: Получение бронирования по `book_ref`.
- **Метод**: GET
- **URL**: `http://0.0.0.0:5002/bookings/ABC123`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  {
    "book_ref": "ABC123",
    "book_date": "2025-01-01",
    "total_amount": 150.50
  }
  ```
- **Ожидаемый ответ** (404 Not Found, если бронирование не найдено):
  ```json
  {
    "message": "Booking not found"
  }
  ```
- **Пояснение**: Тестируйте с существующим `book_ref` (например, `ABC123`) и несуществующим (например, `XYZ999`) для проверки обработки ошибок.

#### 3. POST /bookings
- **Описание**: Создание нового бронирования.
- **Метод**: POST
- **URL**: `http://0.0.0.0:5002/bookings`
- **Тело запроса**:
  ```json
  {
    "book_ref": "GHI789",
    "book_date": "2025-03-15",
    "total_amount": 300.25
  }
  ```
- **Ожидаемый ответ** (201 Created):
  ```json
  {
    "book_ref": "GHI789",
    "book_date": "2025-03-15",
    "total_amount": 300.25
  }
  ```
- **Пояснение**: Убедитесь, что `book_ref` уникален, иначе возникнет ошибка уникальности первичного ключа. `book_date` должен быть в формате `YYYY-MM-DD`.

#### 4. PUT /bookings/<book_ref>
- **Описание**: Обновление бронирования по `book_ref`.
- **Метод**: PUT
- **URL**: `http://0.0.0.0:5002/bookings/ABC123`
- **Тело запроса**:
  ```json
  {
    "book_date": "2025-01-02",
    "total_amount": 175.00
  }
  ```
- **Ожидаемый ответ** (200 OK):
  ```json
  {
    "book_ref": "ABC123",
    "book_date": "2025-01-02",
    "total_amount": 175.00
  }
  ```
- **Ожидаемый ответ** (404 Not Found, если бронирование не найдено):
  ```json
  {
    "message": "Booking not found"
  }
  ```
- **Пояснение**: Тестируйте с существующим `book_ref` и несуществующим для проверки ошибки.

#### 5. DELETE /bookings/<book_ref>
- **Описание**: Удаление бронирования по `book_ref`.
- **Метод**: DELETE
- **URL**: `http://0.0.0.0:5002/bookings/ABC123`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  {
    "book_ref": "ABC123",
    "book_date": "2025-01-02",
    "total_amount": 175.00
  }
  ```
- **Ожидаемый ответ** (404 Not Found, если бронирование не найдено):
  ```json
  {
    "message": "Booking not found"
  }
  ```
- **Пояснение**: После успешного удаления запись возвращается в ответе. Повторный запрос на тот же `book_ref` должен вернуть 404.

#### 6. GET /chesk
- **Описание**: Получение статистики по местам в самолетах.
- **Метод**: GET
- **URL**: `http://0.0.0.0:5002/chesk`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  [
    {
      "aircraft_code": "737",
      "fare_conditions": "Economy",
      "count": 120
    },
    {
      "aircraft_code": "737",
      "fare_conditions": "Business",
      "count": 20
    },
    {
      "aircraft_code": "A320",
      "fare_conditions": "Economy",
      "count": 150
    }
  ]
  ```
- **Пояснение**: Возвращает группированные данные по `aircraft_code` и `fare_conditions` с количеством мест. Ограничение в 100 записей применяется автоматически.

#### 7. POST /aircrafts
- **Описание**: Добавление нового самолета.
- **Метод**: POST
- **URL**: `http://0.0.0.0:5002/aircrafts`
- **Тело запроса**:
  ```json
  {
    "aircraft_code": "A321",
    "model": {"en": "Airbus A321", "ru": "Аэробус А321"},
    "range": 5600
  }
  ```
- **Ожидаемый ответ** (201 Created):
  ```json
  {
    "message": "Aircraft added successfully"
  }
  ```
- **Пояснение**: `aircraft_code` должен быть уникальным. Поле `model` — JSON-объект, а `range` — целое число (в километрах).

#### 8. GET /flights
- **Описание**: Получение информации о рейсах с INNER JOIN.
- **Метод**: GET
- **URL**: `http://0.0.0.0:5002/flights?limit=5`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  [
    {
      "flight_id": 1,
      "flight_no": "PG0401",
      "scheduled_departure": "2025-08-01",
      "scheduled_arrival": "2025-08-01",
      "departure_airport": {"en": "Sheremetyevo", "ru": "Шереметьево"},
      "arrival_airport": {"en": "Domodedovo", "ru": "Домодедово"},
      "aircraft_model": {"en": "Boeing 737", "ru": "Боинг 737"}
    },
    {
      "flight_id": 2,
      "flight_no": "PG0402",
      "scheduled_departure": "2025-08-02",
      "scheduled_arrival": "2025-08-02",
      "departure_airport": {"en": "Vnukovo", "ru": "Внуково"},
      "arrival_airport": {"en": "Pulkovo", "ru": "Пулково"},
      "aircraft_model": {"en": "Airbus A320", "ru": "Аэробус А320"}
    }
  ]
  ```
- **Пояснение**: Параметр `limit` в URL ограничивает количество возвращаемых записей (по умолчанию 10). Ответ включает данные из таблиц `flights`, `airports`, и `aircrafts_data`.

#### 9. GET /bookings_left
- **Описание**: Получение бронирований с LEFT JOIN на таблицу `tickets`.
- **Метод**: GET
- **URL**: `http://0.0.0.0:5002/bookings_left?limit=5`
- **Тело запроса**: Не требуется.
- **Ожидаемый ответ** (200 OK):
  ```json
  [
    {
      "book_ref": "ABC123",
      "book_date": "2025-01-01",
      "total_amount": 150.50,
      "ticket_no": "TCK12345",
      "passenger_id": "1234567890",
      "passenger_name": "John Doe"
    },
    {
      "book_ref": "DEF456",
      "book_date": "2025-02-01",
      "total_amount": 200.75,
      "ticket_no": null,
      "passenger_id": null,
      "passenger_name": null
    }
  ]
  ```
- **Пояснение**: Возвращает бронирования с информацией о билетах (или `null`, если билетов нет). Параметр `limit` ограничивает количество записей.

### Инструкции для Postman
1. **Создание коллекции**:
   - В Postman создайте новую коллекцию (например, `Booking API`).
   - Добавьте запросы для каждого эндпоинта, используя указанные методы, URL и тела запросов.

2. **Настройка заголовков**:
   - Для `POST` и `PUT` установите заголовок `Content-Type: application/json` в разделе Headers.

3. **Тестирование**:
   - Начните с `POST /bookings` для создания тестовых бронирований.
   - Используйте `GET /bookings` для проверки созданных записей.
   - Тестируйте `PUT` и `DELETE` с существующими и несуществующими `book_ref`.
   - Для `/aircrafts` используйте уникальные `aircraft_code`.
   - Для `/flights` и `/bookings_left` экспериментируйте с параметром `limit` (например, `?limit=5` или `?limit=20`).
   - Для `/chesk` проверьте, что возвращаются агрегированные данные.

4. **Ожидаемые ошибки**:
   - Если `book_ref` уже существует при `POST /bookings`, вернется ошибка базы данных (нарушение уникальности).
   - Для несуществующих `book_ref` в `GET`, `PUT`, `DELETE` ожидается 404.
   - Убедитесь, что данные для `/aircrafts` содержат корректный JSON для `model` и числовое значение для `range`.

### Замечания
- Перед тестированием убедитесь, что база данных содержит необходимые таблицы и, при необходимости, начальные данные (например, для `flights`, `airports`, `aircrafts_data`, `seats`, `tickets`).
- Если база данных пуста, некоторые `GET`-запросы (например, `/flights`, `/chesk`, `/bookings_left`) могут вернуть пустой массив.
- Формат даты (`YYYY-MM-DD`) важен для полей `book_date`, `scheduled_departure`, и `scheduled_arrival`.
- Для автоматизации тестирования в Postman можно написать тесты (вкладка Tests), проверяющие коды ответа (200, 201, 404) и структуру JSON.

Эти данные охватывают все эндпоинты и подходят для полноценного тестирования API в Postman. Если нужны дополнительные примеры или помощь с настройкой Postman, дайте знать!


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

Так же визульно можно посмотреть на http://127.0.0.1:5001
