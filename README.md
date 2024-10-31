# API Documentation

___________________________________________________________________
## Запуск

    - создайте файл .env, согласно шаблону .env.example
    - docker-compose up --build -d
___________________________________________________________________

## Свагер досутупен по адресу
    - http://localhost:8080/list_api/openapi#/
___________________________________________________________________

## Authentication

### Register User

- **POST** `/list_api/v1/auth/register`
- **Description**: Регистрация нового пользователя.

### User Login

- **POST** `/list_api/v1/auth/login`
- **Description**: Вход пользователя.

### Refresh Token

- **POST** `/list_api/v1/auth/refresh`
- **Description**: Обновление токена доступа.

### Logout

- **POST** `/list_api/v1/auth/logout`
- **Description**: Выход пользователя.
________________________________________________________________

## Tasks

### Create Task

- **POST** `/list_api/v1/tasks`
- **Description**: Создание новой задачи.

### Get Tasks

- **GET** `/list_api/v1/tasks`
- **Description**: Получение списка задач.

### Update Task

- **PUT** `/list_api/v1/tasks/{task_id}`
- **Description**: Обновление задачи по ID.

### Delete Task

- **DELETE** `/list_api/v1/tasks/{task_id}`
- **Description**: Удаление задачи по ID.
________________________________________________________________

