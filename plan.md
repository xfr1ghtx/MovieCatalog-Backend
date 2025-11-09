# План реализации Movie Catalog API

## Стек технологий
- **Backend**: Python 3.11+ + FastAPI
- **База данных**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Миграции**: Alembic
- **Аутентификация**: JWT Bearer (Access + Refresh tokens)
- **Валидация**: Pydantic v2
- **Контейнеризация**: Docker + Docker Compose
- **Веб-интерфейс БД**: pgAdmin 4

## 1. Структура проекта

```
MovieCatalog-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Точка входа FastAPI приложения
│   ├── config.py               # Конфигурация (settings)
│   ├── database.py             # Подключение к БД
│   ├── dependencies.py         # Dependency Injection
│   │
│   ├── models/                 # SQLAlchemy модели
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── review.py
│   │   ├── favorite.py
│   │   └── token.py
│   │
│   ├── schemas/                # Pydantic схемы
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── review.py
│   │   └── token.py
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # /api/account/register, login, logout
│   │   │   ├── user.py         # /api/account/profile
│   │   │   ├── movies.py       # /api/movies/*
│   │   │   ├── favorites.py    # /api/favorites/*
│   │   │   └── reviews.py      # /api/movie/{movieId}/review/*
│   │   └── deps.py             # API dependencies (auth, etc.)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, password hashing
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── services/               # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── movie_service.py
│   │   ├── review_service.py
│   │   └── favorite_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── validators.py
│
├── alembic/                    # Миграции БД
│   ├── versions/
│   └── env.py
│
├── tests/                      # Тесты
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic.ini
└── README.md
```

## 2. Docker Compose конфигурация

### Сервисы:
1. **api** - FastAPI приложение
2. **db** - PostgreSQL база данных
3. **pgadmin** - Веб-интерфейс для управления БД

### docker-compose.yml:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: movie_catalog
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/movie_catalog
      JWT_SECRET_KEY: your-secret-key
      JWT_ALGORITHM: HS256
      ACCESS_TOKEN_EXPIRE_MINUTES: 30
      REFRESH_TOKEN_EXPIRE_DAYS: 7
    depends_on:
      - db
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
```

## 3. Модели базы данных (SQLAlchemy)

### 3.1 User (users)
- id (UUID, PK)
- username (String, unique)
- email (String, unique)
- name (String)
- password_hash (String)
- birth_date (DateTime, nullable)
- gender (Integer, 0/1)
- avatar_link (String, nullable)
- created_at (DateTime)
- updated_at (DateTime)

### 3.2 RefreshToken (refresh_tokens)
- id (UUID, PK)
- user_id (UUID, FK -> users.id)
- token (String, unique)
- expires_at (DateTime)
- created_at (DateTime)

### 3.3 Genre (genres)
- id (UUID, PK)
- name (String, unique)

### 3.4 Movie (movies)
- id (UUID, PK)
- name (String)
- poster (String)
- year (Integer)
- country (String)
- time (Integer) - продолжительность в минутах
- tagline (String, nullable)
- description (Text, nullable)
- director (String, nullable)
- budget (Integer, nullable)
- fees (Integer, nullable)
- age_limit (Integer)
- created_at (DateTime)

### 3.5 MovieGenre (movie_genres) - связь many-to-many
- movie_id (UUID, FK -> movies.id)
- genre_id (UUID, FK -> genres.id)

### 3.6 Review (reviews)
- id (UUID, PK)
- movie_id (UUID, FK -> movies.id)
- user_id (UUID, FK -> users.id)
- rating (Integer, 0-10)
- review_text (Text)
- is_anonymous (Boolean)
- created_at (DateTime)
- updated_at (DateTime)

### 3.7 FavoriteMovie (favorite_movies)
- user_id (UUID, FK -> users.id)
- movie_id (UUID, FK -> movies.id)
- created_at (DateTime)
- Composite PK: (user_id, movie_id)

## 4. Pydantic схемы

### 4.1 Auth схемы
- `UserRegisterModel` - регистрация
- `LoginCredentials` - логин
- `TokenResponse` - ответ с access и refresh токенами

### 4.2 User схемы
- `ProfileModel` - профиль пользователя
- `UserShortModel` - краткая информация о пользователе

### 4.3 Movie схемы
- `MovieElementModel` - элемент списка фильмов
- `MovieDetailsModel` - детальная информация о фильме
- `MoviesListModel` - список фильмов
- `MoviesPagedListModel` - список фильмов с пагинацией
- `PageInfoModel` - информация о пагинации

### 4.4 Review схемы
- `ReviewModel` - отзыв
- `ReviewShortModel` - краткий отзыв (только id и rating)
- `ReviewModifyModel` - создание/редактирование отзыва

### 4.5 Genre схемы
- `GenreModel` - жанр

### 4.6 Enums
- `Gender` - пол (0 - Male, 1 - Female)

## 5. Аутентификация и авторизация

### 5.1 JWT Bearer Authentication
- **Access Token**: короткий срок жизни (30 минут)
- **Refresh Token**: длинный срок жизни (7 дней)
- Хранение refresh токенов в БД для возможности отзыва

### 5.2 Endpoints
- `POST /api/account/register` - регистрация
  - Валидация email, username
  - Хеширование пароля (bcrypt)
  - Создание пользователя
  - Возврат токенов
  
- `POST /api/account/login` - логин
  - Проверка credentials
  - Генерация access и refresh токенов
  - Сохранение refresh token в БД
  
- `POST /api/account/logout` - выход
  - Требует авторизации
  - Удаление refresh token из БД
  
- `POST /api/account/refresh` (дополнительный endpoint)
  - Обновление access token по refresh token

### 5.3 Security
- Хеширование паролей: `bcrypt`
- JWT библиотека: `python-jose[cryptography]`
- Dependency для проверки авторизации: `get_current_user`

## 6. API Endpoints

### 6.1 Auth (/api/account)
- ✅ `POST /register` - регистрация
- ✅ `POST /login` - вход
- ✅ `POST /logout` - выход
- ➕ `POST /refresh` - обновление токена (дополнительно)

### 6.2 User (/api/account)
- ✅ `GET /profile` - получить профиль (требует auth)
- ✅ `PUT /profile` - обновить профиль (требует auth)

### 6.3 Movies (/api/movies)
- ✅ `GET /{page}` - список фильмов с пагинацией
  - Default page = 1
  - Page size = 6 (настраиваемо)
  - Возврат: movies + pageInfo
  
- ✅ `GET /details/{id}` - детали фильма
  - UUID фильма
  - Включает все отзывы

### 6.4 Favorites (/api/favorites)
- ✅ `GET /` - список избранных фильмов (требует auth)
- ✅ `POST /{id}/add` - добавить в избранное (требует auth)
- ✅ `DELETE /{id}/delete` - удалить из избранного (требует auth)

### 6.5 Reviews (/api/movie)
- ✅ `POST /{movieId}/review/add` - добавить отзыв (требует auth)
  - Валидация: rating 0-10
  - Один пользователь = один отзыв на фильм
  
- ✅ `PUT /{movieId}/review/{id}/edit` - редактировать отзыв (требует auth)
  - Только автор может редактировать
  
- ✅ `DELETE /{movieId}/review/{id}/delete` - удалить отзыв (требует auth)
  - Только автор может удалять

## 7. Бизнес-логика и валидация

### 7.1 Валидации
- Email формат и уникальность
- Username уникальность
- Password сложность (минимум 6 символов)
- Rating: 0-10
- UUID формат для всех ID
- Дата рождения в прошлом

### 7.2 Правила
- Один пользователь может оставить только один отзыв на фильм
- Пользователь может редактировать/удалять только свои отзывы
- Anonymous отзывы: не показывать автора (null в UserShortModel)
- Избранное: уникальная пара (user_id, movie_id)

### 7.3 Обработка ошибок
- 400 Bad Request - невалидные данные
- 401 Unauthorized - не авторизован
- 403 Forbidden - нет прав доступа
- 404 Not Found - ресурс не найден
- 409 Conflict - конфликт (например, дубликат)
- 500 Internal Server Error - ошибка сервера

## 8. Swagger UI

### Конфигурация в FastAPI:
```python
app = FastAPI(
    title="MovieCatalog.API",
    version="v1",
    docs_url="/swagger",
    redoc_url="/redoc",
    openapi_url="/swagger.json"
)
```

### Доступ:
- Swagger UI: `http://localhost:8000/swagger`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/swagger.json`

### Security Scheme:
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()
```

## 9. Веб-интерфейс БД (pgAdmin)

### Настройка:
- URL: `http://localhost:5050`
- Email: `admin@admin.com`
- Password: `admin`

### Подключение к БД:
- Host: `db` (имя сервиса в Docker)
- Port: `5432`
- Database: `movie_catalog`
- Username: `postgres`
- Password: `postgres`

## 10. Миграции базы данных (Alembic)

### Команды:
```bash
# Создать миграцию
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Первоначальная миграция включает:
1. Создание таблицы users
2. Создание таблицы refresh_tokens
3. Создание таблицы genres
4. Создание таблицы movies
5. Создание таблицы movie_genres
6. Создание таблицы reviews
7. Создание таблицы favorite_movies
8. Индексы и внешние ключи

## 11. Зависимости (requirements.txt)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

## 12. Переменные окружения (.env)

```
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movie_catalog

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
API_V1_PREFIX=/api
PROJECT_NAME=MovieCatalog.API

# CORS (если нужно)
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## 13. Этапы реализации

### Этап 1: Настройка инфраструктуры
1. ✅ Создать структуру проекта
2. ✅ Настроить Docker Compose (PostgreSQL, pgAdmin)
3. ✅ Создать Dockerfile для API
4. ✅ Настроить requirements.txt
5. ✅ Настроить переменные окружения

### Этап 2: База данных
1. ✅ Создать SQLAlchemy модели
2. ✅ Настроить Alembic
3. ✅ Создать первоначальную миграцию
4. ✅ Применить миграции
5. ✅ Добавить seed данные (жанры, тестовые фильмы)

### Этап 3: Аутентификация
1. ✅ Реализовать JWT utilities (generate, verify)
2. ✅ Реализовать password hashing
3. ✅ Создать auth dependencies (get_current_user)
4. ✅ Реализовать endpoints: register, login, logout
5. ✅ Реализовать refresh token механизм

### Этап 4: User API
1. ✅ Создать Pydantic схемы для пользователя
2. ✅ Реализовать GET /api/account/profile
3. ✅ Реализовать PUT /api/account/profile

### Этап 5: Movies API
1. ✅ Создать Pydantic схемы для фильмов
2. ✅ Реализовать GET /api/movies/{page}
3. ✅ Реализовать пагинацию
4. ✅ Реализовать GET /api/movies/details/{id}

### Этап 6: Favorites API
1. ✅ Создать Pydantic схемы
2. ✅ Реализовать GET /api/favorites
3. ✅ Реализовать POST /api/favorites/{id}/add
4. ✅ Реализовать DELETE /api/favorites/{id}/delete

### Этап 7: Reviews API
1. ✅ Создать Pydantic схемы для отзывов
2. ✅ Реализовать POST /api/movie/{movieId}/review/add
3. ✅ Реализовать PUT /api/movie/{movieId}/review/{id}/edit
4. ✅ Реализовать DELETE /api/movie/{movieId}/review/{id}/delete
5. ✅ Добавить валидации (один отзыв на фильм, только автор может редактировать)

### Этап 8: Тестирование и документация
1. ✅ Проверить Swagger UI
2. ✅ Протестировать все endpoints
3. ✅ Добавить обработку ошибок
4. ✅ Написать README.md с инструкциями
5. ✅ (Опционально) Написать unit тесты

### Этап 9: Деплой
1. ✅ Проверить работу в Docker
2. ✅ Настроить production переменные
3. ✅ Добавить CORS при необходимости
4. ✅ Настроить логирование

## 14. Дополнительные улучшения (опционально)

- Rate limiting для API
- Кэширование (Redis) для списка фильмов
- Загрузка изображений (S3/MinIO)
- Полнотекстовый поиск фильмов
- Фильтрация по жанрам, году
- Сортировка фильмов
- Pagination cursor-based вместо offset-based
- WebSocket для real-time уведомлений
- CI/CD pipeline
- Мониторинг (Prometheus + Grafana)

## 15. Безопасность

- ✅ HTTPS в production
- ✅ Секретные ключи в переменных окружения
- ✅ SQL injection защита (SQLAlchemy ORM)
- ✅ CORS правильная настройка
- ✅ Rate limiting
- ✅ Input validation (Pydantic)
- ✅ Password complexity requirements
- ✅ JWT token rotation
- ✅ Secure password hashing (bcrypt)

## 16. Начало работы

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd MovieCatalog-Backend

# 2. Создать .env файл
cp .env.example .env
# Отредактировать .env

# 3. Запустить Docker Compose
docker-compose up -d

# 4. Применить миграции
docker-compose exec api alembic upgrade head

# 5. (Опционально) Загрузить seed данные
docker-compose exec api python -m app.seed

# 6. Открыть Swagger
# http://localhost:8000/swagger

# 7. Открыть pgAdmin
# http://localhost:5050
```

---

**Статус**: План готов к реализации
**Версия**: 1.0
**Дата**: 2025-11-09

