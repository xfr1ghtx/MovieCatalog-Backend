# Архитектура MovieCatalog API

## Общая схема

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser/Mobile)                │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         API GATEWAY                          │
│                    FastAPI Application                       │
│                    (Port 8000)                              │
└─────────────────────────────┬───────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Auth Routes   │    │ Movies Routes │    │ Review Routes │
│ /api/account  │    │ /api/movies   │    │ /api/movie    │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Auth     │  │   Movie    │  │   Review   │           │
│  │  Service   │  │  Service   │  │  Service   │  ...      │
│  └────────────┘  └────────────┘  └────────────┘           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER (ORM)                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │  User   │  │  Movie  │  │ Review  │  │  Genre  │ ...  │
│  │ Model   │  │  Model  │  │  Model  │  │  Model  │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      PostgreSQL Database                     │
│                         (Port 5432)                          │
└─────────────────────────────────────────────────────────────┘
```

## Поток данных

### 1. Регистрация пользователя

```
Client
  │
  │ POST /api/account/register
  │ {username, email, password, ...}
  ▼
AuthRouter (auth.py)
  │
  │ Validation (Pydantic)
  ▼
AuthService
  │
  ├─► Check username exists
  ├─► Check email exists
  ├─► Hash password (bcrypt)
  ├─► Create user
  └─► Generate JWT tokens
      │
      ▼
User Model → PostgreSQL
      │
      ▼
Response {token: "..."}
```

### 2. Добавление отзыва (с авторизацией)

```
Client
  │
  │ POST /api/movie/{id}/review/add
  │ Header: Authorization: Bearer {token}
  │ Body: {reviewText, rating, isAnonymous}
  ▼
Middleware: get_current_user
  │
  ├─► Decode JWT token
  ├─► Verify token signature
  ├─► Extract user_id
  └─► Load user from DB
      │
      ▼
ReviewRouter (reviews.py)
  │
  │ Validation (Pydantic)
  ▼
ReviewService
  │
  ├─► Check movie exists
  ├─► Check user hasn't reviewed
  └─► Create review
      │
      ▼
Review Model → PostgreSQL
      │
      ▼
Response {message: "Success"}
```

### 3. Получение списка фильмов

```
Client
  │
  │ GET /api/movies/1
  ▼
MoviesRouter (movies.py)
  │
  ▼
MovieService
  │
  ├─► Calculate pagination
  ├─► Query movies from DB
  ├─► Load related genres
  ├─► Load related reviews
  └─► Format response
      │
      ▼
Movie Model → PostgreSQL
      │
      ▼
Response {movies: [...], pageInfo: {...}}
```

## Компоненты системы

### API Layer (`app/api/`)

Отвечает за:
- Прием HTTP запросов
- Валидацию входных данных (Pydantic)
- Авторизацию (JWT)
- Формирование HTTP ответов
- Обработку ошибок

**Файлы:**
- `deps.py` - Dependency Injection (get_current_user)
- `routes/auth.py` - Аутентификация
- `routes/user.py` - Профиль
- `routes/movies.py` - Фильмы
- `routes/favorites.py` - Избранное
- `routes/reviews.py` - Отзывы

### Service Layer (`app/services/`)

Отвечает за:
- Бизнес-логику приложения
- Работу с несколькими моделями
- Валидацию бизнес-правил
- Транзакции

**Файлы:**
- `auth_service.py` - Регистрация, вход, выход
- `user_service.py` - Управление профилем
- `movie_service.py` - Работа с фильмами
- `favorite_service.py` - Избранное
- `review_service.py` - Отзывы

### Data Layer (`app/models/`)

Отвечает за:
- Определение структуры БД
- ORM маппинг (SQLAlchemy)
- Связи между таблицами
- Constraints и индексы

**Файлы:**
- `user.py` - Пользователи
- `token.py` - Refresh токены
- `genre.py` - Жанры
- `movie.py` - Фильмы
- `review.py` - Отзывы
- `favorite.py` - Избранное

### Validation Layer (`app/schemas/`)

Отвечает за:
- Валидацию входных данных
- Сериализацию/десериализацию
- API контракты
- Type hints

**Файлы:**
- `auth.py` - Схемы аутентификации
- `user.py` - Схемы пользователя
- `movie.py` - Схемы фильмов
- `review.py` - Схемы отзывов
- `token.py` - Схемы токенов

### Core Layer (`app/core/`)

Отвечает за:
- JWT токены
- Хеширование паролей
- Custom exceptions
- Общие утилиты

**Файлы:**
- `security.py` - JWT, bcrypt
- `exceptions.py` - Custom exceptions

## База данных

### ER диаграмма

```
┌──────────────┐
│    users     │
├──────────────┤
│ id (PK)      │───┐
│ username     │   │
│ email        │   │
│ password_hash│   │
│ name         │   │
│ birth_date   │   │
│ gender       │   │
│ avatar_link  │   │
└──────────────┘   │
                   │
     ┌─────────────┼─────────────┐
     │             │             │
     ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│refresh_tokens│ │   reviews    │ │favorite_movies│
├──────────────┤ ├──────────────┤ ├──────────────┤
│ id (PK)      │ │ id (PK)      │ │user_id (PK,FK)│
│ user_id (FK) │ │ user_id (FK) │ │movie_id(PK,FK)│
│ token        │ │ movie_id (FK)│ └──────────────┘
│ expires_at   │ │ rating       │        │
└──────────────┘ │ review_text  │        │
                 │ is_anonymous │        │
                 └──────────────┘        │
                        │                │
          ┌─────────────┴────────────────┘
          │
          ▼
    ┌──────────────┐
    │   movies     │
    ├──────────────┤
    │ id (PK)      │───┐
    │ name         │   │
    │ poster       │   │
    │ year         │   │
    │ country      │   │
    │ time         │   │
    │ tagline      │   │
    │ description  │   │
    │ director     │   │
    │ budget       │   │
    │ fees         │   │
    │ age_limit    │   │
    └──────────────┘   │
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            │            ▼
    ┌──────────────┐   │     ┌──────────────┐
    │ movie_genres │   │     │   genres     │
    ├──────────────┤   │     ├──────────────┤
    │movie_id(PK,FK)│  │     │ id (PK)      │
    │genre_id(PK,FK)│──┘     │ name         │
    └──────────────┘         └──────────────┘
```

### Ключевые связи

1. **User → Reviews (1:N)**
   - Один пользователь может оставить много отзывов
   - При удалении пользователя удаляются его отзывы (CASCADE)

2. **Movie → Reviews (1:N)**
   - У фильма может быть много отзывов
   - При удалении фильма удаляются отзывы (CASCADE)

3. **Movie ↔ Genres (N:M)**
   - У фильма может быть несколько жанров
   - Жанр может быть у многих фильмов
   - Связь через таблицу `movie_genres`

4. **User ↔ Movies (N:M через FavoriteMovies)**
   - Пользователь может добавить много фильмов в избранное
   - Фильм может быть в избранном у многих пользователей

## Аутентификация и авторизация

### JWT Flow

```
1. Registration/Login
   ┌────────┐                     ┌────────┐
   │ Client │────register/login──►│  API   │
   └────────┘                     └────┬───┘
       ▲                               │
       │                               │ Create JWT
       │                               │ (user_id, exp)
       │                               ▼
       │                          ┌────────┐
       └────────{token}───────────│Database│
                                  └────────┘
                                  Store refresh_token

2. Protected Request
   ┌────────┐                     ┌────────┐
   │ Client │──Header: Bearer──►  │  API   │
   └────────┘     {token}         └────┬───┘
       ▲                               │
       │                               │ Verify JWT
       │                               │ - Signature
       │                               │ - Expiration
       │                               │ - Extract user_id
       │                               ▼
       │                          ┌────────┐
       │                          │Database│
       │                          └────┬───┘
       │                               │
       │                               │ Load User
       └───────Response with data──────┘
```

### Token структура

**Access Token** (срок жизни: 30 минут):
```json
{
  "sub": "user-uuid",
  "exp": 1699999999,
  "type": "access"
}
```

**Refresh Token** (срок жизни: 7 дней):
```json
{
  "sub": "user-uuid",
  "exp": 1699999999,
  "type": "refresh"
}
```

## Обработка ошибок

### Иерархия исключений

```
HTTPException (FastAPI)
    │
    ├─► BadRequestException (400)
    │   └─ Невалидные входные данные
    │
    ├─► UnauthorizedException (401)
    │   └─ Не авторизован / Невалидный токен
    │
    ├─► ForbiddenException (403)
    │   └─ Нет прав на действие
    │
    ├─► NotFoundException (404)
    │   └─ Ресурс не найден
    │
    └─► ConflictException (409)
        └─ Конфликт (дубликат)
```

### Пример обработки

```python
try:
    # Business logic
    user = create_user(data)
except IntegrityError:
    raise ConflictException("User already exists")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(500, "Internal server error")
```

## Безопасность

### Защитные механизмы

1. **Password Security**
   - Bcrypt hashing (cost factor 12)
   - Никогда не храним plain-text пароли
   - Минимум 6 символов

2. **JWT Security**
   - HMAC-SHA256 подпись
   - Short-lived access tokens (30 min)
   - Refresh tokens в БД (можно отозвать)

3. **SQL Injection Protection**
   - SQLAlchemy ORM
   - Prepared statements
   - Параметризованные запросы

4. **Input Validation**
   - Pydantic схемы
   - Type checking
   - Custom validators

5. **Authorization**
   - JWT Bearer tokens
   - Проверка на каждый защищенный endpoint
   - User context injection

## Производительность

### Оптимизации

1. **Database**
   - Индексы на foreign keys
   - Индексы на часто используемых полях (username, email)
   - Eager loading для связанных данных

2. **API**
   - Пагинация списков
   - Селективная загрузка полей
   - HTTP кэширование заголовки

3. **Connection Pooling**
   - SQLAlchemy pool
   - Reuse connections
   - Max overflow control

### Потенциальные узкие места

1. **N+1 queries** - используем eager loading
2. **Large result sets** - используем pagination
3. **Expensive joins** - можем добавить денормализацию
4. **No caching** - можем добавить Redis

## Мониторинг и логирование

### Логирование (текущее)

- FastAPI access logs
- SQLAlchemy query logs (debug mode)
- Python logging framework

### Можно добавить

- Structured logging (JSON)
- Log aggregation (ELK)
- Distributed tracing
- Metrics (Prometheus)
- APM (Application Performance Monitoring)

## Масштабирование

### Горизонтальное масштабирование

```
┌───────────┐
│   Nginx   │ Load Balancer
└─────┬─────┘
      │
      ├─────────────┬─────────────┐
      ▼             ▼             ▼
  ┌────────┐   ┌────────┐   ┌────────┐
  │ API #1 │   │ API #2 │   │ API #3 │
  └────┬───┘   └────┬───┘   └────┬───┘
       │            │            │
       └────────────┴────────────┘
                    ▼
            ┌──────────────┐
            │ PostgreSQL   │
            │  (Primary)   │
            └──────┬───────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌─────────┐         ┌─────────┐
    │ Replica │         │ Replica │
    │  (Read) │         │  (Read) │
    └─────────┘         └─────────┘
```

### Возможности масштабирования

- ✅ Stateless API (можно запускать множество инстансов)
- ✅ JWT в header (не session storage)
- ✅ Database pooling
- ⚠️ Нужен shared cache (Redis)
- ⚠️ Нужен message queue для async tasks

---

**Архитектура спроектирована с учетом:**
- Clean Architecture принципов
- SOLID принципов
- RESTful API best practices
- Security best practices
- Scalability considerations

