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
