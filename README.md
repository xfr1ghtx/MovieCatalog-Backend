# MovieCatalog-Backend

Backend API для каталога фильмов, разработанный на FastAPI с PostgreSQL.

## Стек технологий

- **Backend**: Python 3.11+ + FastAPI
- **База данных**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Миграции**: Alembic
- **Аутентификация**: JWT Bearer (Access + Refresh tokens)
- **Валидация**: Pydantic v2
- **Контейнеризация**: Docker + Docker Compose
- **Веб-интерфейс БД**: pgAdmin 4

## Возможности API

### Аутентификация
- ✅ Регистрация пользователей
- ✅ Вход/выход
- ✅ JWT токены (Access + Refresh)

### Управление профилем
- ✅ Просмотр профиля
- ✅ Обновление профиля

### Фильмы
- ✅ Список фильмов с пагинацией
- ✅ Детальная информация о фильме
- ✅ Жанры фильмов

### Избранное
- ✅ Список избранных фильмов
- ✅ Добавление в избранное
- ✅ Удаление из избранного

### Отзывы
- ✅ Добавление отзыва
- ✅ Редактирование отзыва
- ✅ Удаление отзыва
- ✅ Анонимные отзывы

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонировать репозиторий**
```bash
git clone <repository-url>
cd MovieCatalog-Backend
```

2. **Создать файл .env**
```bash
# Скопируйте .env.example и отредактируйте при необходимости
# Для быстрого старта можно использовать настройки по умолчанию
```

3. **Запустить Docker Compose**
```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL на порту 5432
- FastAPI приложение на порту 8000
- pgAdmin на порту 5050

4. **Применить миграции базы данных**
```bash
docker-compose exec api alembic upgrade head
```

5. **Загрузить тестовые данные (опционально)**
```bash
docker-compose exec api python -m app.seed
```

6. **Проверить работу API**
- Swagger UI: http://localhost:8000/swagger
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Доступ к pgAdmin

1. Откройте http://localhost:5050
2. Войдите с учетными данными:
   - Email: `admin@admin.com`
   - Password: `admin`
3. Подключитесь к БД:
   - Host: `db`
   - Port: `5432`
   - Database: `movie_catalog`
   - Username: `postgres`
   - Password: `postgres`

## Структура проекта

```
MovieCatalog-Backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── routes/
│   │   │   ├── auth.py         # Аутентификация
│   │   │   ├── user.py         # Профиль пользователя
│   │   │   ├── movies.py       # Фильмы
│   │   │   ├── favorites.py    # Избранное
│   │   │   └── reviews.py      # Отзывы
│   │   └── deps.py             # Зависимости API
│   ├── core/
│   │   ├── security.py         # JWT, хеширование паролей
│   │   └── exceptions.py       # Кастомные исключения
│   ├── models/                 # SQLAlchemy модели
│   ├── schemas/                # Pydantic схемы
│   ├── services/               # Бизнес-логика
│   ├── config.py               # Конфигурация
│   ├── database.py             # Подключение к БД
│   ├── main.py                 # Точка входа FastAPI
│   └── seed.py                 # Seed данные
├── alembic/                    # Миграции БД
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

### Аутентификация (`/api/account`)
- `POST /register` - Регистрация
- `POST /login` - Вход
- `POST /logout` - Выход

### Профиль (`/api/account`)
- `GET /profile` - Получить профиль (требует авторизации)
- `PUT /profile` - Обновить профиль (требует авторизации)

### Фильмы (`/api/movies`)
- `GET /{page}` - Список фильмов с пагинацией
- `GET /details/{id}` - Детали фильма

### Избранное (`/api/favorites`)
- `GET /` - Список избранных (требует авторизации)
- `POST /{id}/add` - Добавить в избранное (требует авторизации)
- `DELETE /{id}/delete` - Удалить из избранного (требует авторизации)

### Отзывы (`/api/movie`)
- `POST /{movieId}/review/add` - Добавить отзыв (требует авторизации)
- `PUT /{movieId}/review/{id}/edit` - Редактировать отзыв (требует авторизации)
- `DELETE /{movieId}/review/{id}/delete` - Удалить отзыв (требует авторизации)

## Разработка

### Локальная разработка без Docker

1. **Создать виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. **Установить зависимости**
```bash
pip install -r requirements.txt
```

3. **Создать .env файл с настройками**
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movie_catalog
JWT_SECRET_KEY=your-secret-key
```

4. **Применить миграции**
```bash
alembic upgrade head
```

5. **Запустить сервер**
```bash
uvicorn app.main:app --reload
```

### Работа с миграциями

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1

# Посмотреть текущую версию
alembic current
```

## Безопасность

- ✅ JWT токены для аутентификации
- ✅ Хеширование паролей с bcrypt
- ✅ Валидация входных данных с Pydantic
- ✅ Защита от SQL injection через SQLAlchemy ORM
- ✅ CORS настройки

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgresql://postgres:postgres@localhost:5432/movie_catalog` |
| `JWT_SECRET_KEY` | Секретный ключ для JWT | - |
| `JWT_ALGORITHM` | Алгоритм JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни access токена | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Время жизни refresh токена | `7` |

## Остановка и удаление

```bash
# Остановить контейнеры
docker-compose down

# Остановить и удалить volumes (база данных будет удалена!)
docker-compose down -v
```

## Лицензия

This server application was developed for laboratory work on the subject "Fundamentals of Mobile Development" in the undergraduate program HITs TSU
