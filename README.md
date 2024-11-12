# Flask_SQL

скачать нужну базу данных по ссылки:

https://postgrespro.ru/education/demodb

положить в папку с проектом переименовав ее в db.sql

у вас должен быть уставлен docker и docker-compose
запустить развертку postgres и зальет вашу db


```
docker-compose up -d
```

накатить дамп
```
docker exec -i postgres_demo psql -U postgres -d demo < db.sql
```



подколючиться в контйнере к
docker exec -it postgres_demo psql -U postgres -d demo
посмотреть
\dt


## Тестирование маршрутов:

Получение всех бронирований:

bash
Copy
curl http://localhost:5000/bookings
Получение бронирования по book_ref:

bash
Copy
curl http://localhost:5000/bookings/<book_ref>
Создание нового бронирования:

bash
Copy
curl -X POST -H "Content-Type: application/json" -d '{"book_ref": "123456", "book_date": "2023-11-12", "total_amount": 1000}' http://localhost:5000/bookings
Обновление бронирования:

bash
Copy
curl -X PUT -H "Content-Type: application/json" -d '{"book_date": "2023-11-13", "total_amount": 1200}' http://localhost:5000/bookings/123456
Удаление бронирования:

bash
Copy
curl -X DELETE http://localhost:5000/bookings/123456
