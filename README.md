# technical_task

## Запуск проекта 

1. Склонируйте репорзиторий.
2. Создайте .env файл в каталоге infra/envs по примеру .env.example
3. Запустите Docker, если он не запущен
4. Находяся в папке infra выполните docker compose up -d --build
5. Подождите пока выполнятсья миграции, соберетсья статика и создаться суперпользователь
6. Админка доступна по адресу  http://localhost/admin/
    - username: admin
    - password: 123


## Ручки

----------------------------------------------------------------
GET http://localhost/api/v1/trainers/
```json
[
    {
        "id": 1,
        "first_name": "Алексей",
        "last_name": "Нестеров",
        "date_of_birth": "1924-03-12",
        "gender": "man",
        "description": "Первый тренер",
        "gyms": [
            1
        ]
    }
]
```
--------------------------------------------------------


- GET http://localhost/api/v1/users/
----------------------------------------------------------------
```json
[
    {
        "id": 1,
        "name": "Марина",
        "last_name": "Зайцева",
        "email": "best@ma.ru",
        "password": "432",
        "phone_number": "9210649216491"
    },
    {
        "id": 2,
        "name": "Дарья",
        "last_name": "Гаври",
        "email": "best@one.ru",
        "password": "442",
        "phone_number": "421441424"
    }
]
```
--------------------------------


- POST http://localhost/api/v1/records/
----------------------------------------------------------------
- Запрос
```json
{
  "client": 1,  // ID клиента (User), который делает запись
  "trainer": 1,  // ID тренера (Trainer), с которым делается запись
  "schedule": 2  // ID расписания (Schedule), на которое делается запись
}
```


- Ответ
```json
{
    "id": 3,
    "client": {
        "id": 1,
        "name": "Марина",
        "last_name": "Зайцева",
        "email": "best@ma.ru",
        "password": "432",
        "phone_number": "9210649216491"
    },
    "trainer": {
        "id": 1,
        "first_name": "Алексей",
        "last_name": "Нестеров",
        "date_of_birth": "1924-03-12",
        "gender": "man",
        "description": "Первый тренер",
        "gyms": [
            1
        ]
    },
    "schedule": {
        "id": 1,
        "day": "monday",
        "start_time": "16:48:41",
        "end_time": "17:26:44",
        "trainer": 1,
        "gym": 1
    }
}
```


- Если такая запись уже есть то
```json
{
    "__all__": [
        "Эта запись уже существует.",
        "Запись with this Trainer and Schedule already exists."
    ]
}
```
----------------------------------------------------------------
