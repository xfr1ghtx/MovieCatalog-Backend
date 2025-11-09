# Быстрый старт MovieCatalog Backend

## Шаг 1: Запуск с Docker Compose (Рекомендуется)

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить статус контейнеров
docker-compose ps

# Применить миграции БД
docker-compose exec api alembic upgrade head

# Загрузить тестовые данные (фильмы и жанры)
docker-compose exec api python -m app.seed
```

## Шаг 2: Проверка работы

### API документация (Swagger)
Откройте в браузере: http://localhost:8000/swagger

### Тестовый запрос
```bash
curl http://localhost:8000/health
```

Ответ должен быть: `{"status":"healthy"}`

### Список фильмов
```bash
curl http://localhost:8000/api/movies/1
```

## Шаг 3: Регистрация пользователя

### Через Swagger UI
1. Откройте http://localhost:8000/swagger
2. Найдите endpoint `POST /api/account/register`
3. Нажмите "Try it out"
4. Заполните JSON:
```json
{
  "userName": "testuser",
  "name": "Test User",
  "password": "password123",
  "email": "test@example.com",
  "birthDate": "2000-01-01T00:00:00",
  "gender": 0
}
```
5. Нажмите "Execute"
6. Скопируйте полученный token

### Через curl
```bash
curl -X POST "http://localhost:8000/api/account/register" \
  -H "Content-Type: application/json" \
  -d '{
    "userName": "testuser",
    "name": "Test User",
    "password": "password123",
    "email": "test@example.com",
    "birthDate": "2000-01-01T00:00:00",
    "gender": 0
  }'
```

## Шаг 4: Авторизация в Swagger

1. Нажмите кнопку "Authorize" в правом верхнем углу Swagger UI
2. Вставьте token (БЕЗ префикса "Bearer")
3. Нажмите "Authorize"
4. Теперь вы можете использовать защищенные endpoints!

## Шаг 5: Тестирование основных функций

### Получить профиль
```bash
curl -X GET "http://localhost:8000/api/account/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Добавить фильм в избранное
1. Получите ID фильма из списка: http://localhost:8000/api/movies/1
2. Используйте endpoint `POST /api/favorites/{id}/add`

### Добавить отзыв на фильм
```bash
curl -X POST "http://localhost:8000/api/movie/{MOVIE_ID}/review/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewText": "Отличный фильм!",
    "rating": 10,
    "isAnonymous": false
  }'
```

## Доступ к pgAdmin

1. Откройте http://localhost:5050
2. Войдите:
   - Email: `admin@admin.com`
   - Password: `admin`
3. Добавьте сервер:
   - Name: `MovieCatalog`
   - Host: `db`
   - Port: `5432`
   - Database: `movie_catalog`
   - Username: `postgres`
   - Password: `postgres`

## Полезные команды

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api

# Только база данных
docker-compose logs -f db
```

### Перезапуск сервиса
```bash
docker-compose restart api
```

### Остановка всех сервисов
```bash
docker-compose down
```

### Полная очистка (включая БД!)
```bash
docker-compose down -v
```

## Структура тестовых данных

После выполнения seed скрипта в БД будут:

- **10 жанров**: Драма, Комедия, Боевик, Триллер, Ужасы, Фантастика, Мелодрама, Приключения, Детектив, Фэнтези
- **8 фильмов**: Побег из Шоушенка, Зеленая миля, Форрест Гамп, Начало, Интерстеллар, Матрица, Бойцовский клуб, Престиж

## Решение проблем

### Порт уже занят
Если порты 5432, 8000 или 5050 заняты, измените их в `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Вместо 8000:8000
```

### База данных не подключается
```bash
# Проверить статус контейнера БД
docker-compose ps db

# Пересоздать контейнер БД
docker-compose down
docker-compose up -d db
```

### API не запускается
```bash
# Посмотреть логи
docker-compose logs api

# Пересобрать образ
docker-compose build api
docker-compose up -d api
```

## Дополнительная информация

- Подробная документация: [README.md](README.md)
- План реализации: [plan.md](plan.md)
- Swagger UI: http://localhost:8000/swagger
- ReDoc: http://localhost:8000/redoc

