# API Endpoints Reference

## Аутентификация

### POST /api/account/register
Регистрация нового пользователя.

**Тело запроса:**
```json
{
  "userName": "string",
  "name": "string",
  "password": "string (min 6 символов)",
  "email": "string (email формат)",
  "birthDate": "datetime (optional)",
  "gender": 0 или 1 (0 = Male, 1 = Female)
}
```

**Ответ (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Ошибки:**
- 409: Username или email уже зарегистрированы
- 400: Невалидные данные

---

### POST /api/account/login
Вход в систему.

**Тело запроса:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Ответ (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Ошибки:**
- 401: Неверные учетные данные

---

### POST /api/account/logout
Выход из системы. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Ответ (200):**
```json
{
  "message": "Successfully logged out"
}
```

**Ошибки:**
- 401: Не авторизован

---

## Профиль пользователя

### GET /api/account/profile
Получить профиль текущего пользователя. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Ответ (200):**
```json
{
  "id": "uuid",
  "nickName": "string",
  "email": "string",
  "avatarLink": "string",
  "name": "string",
  "birthDate": "datetime",
  "gender": 0 или 1
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Пользователь не найден

---

### PUT /api/account/profile
Обновить профиль. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Тело запроса:**
```json
{
  "id": "uuid",
  "nickName": "string",
  "email": "string",
  "avatarLink": "string",
  "name": "string",
  "birthDate": "datetime",
  "gender": 0 или 1
}
```

**Ответ (200):**
```json
{
  "id": "uuid",
  "nickName": "string",
  "email": "string",
  "avatarLink": "string",
  "name": "string",
  "birthDate": "datetime",
  "gender": 0 или 1
}
```

**Ошибки:**
- 401: Не авторизован

---

## Фильмы

### GET /api/movies/{page}
Получить список фильмов с пагинацией.

**Параметры:**
- `page` (path, integer, >= 1): Номер страницы

**Ответ (200):**
```json
{
  "movies": [
    {
      "id": "uuid",
      "name": "string",
      "poster": "string (URL)",
      "year": 2024,
      "country": "string",
      "genres": [
        {
          "id": "uuid",
          "name": "string"
        }
      ],
      "reviews": [
        {
          "id": "uuid",
          "rating": 8,
          "reviewText": "string",
          "isAnonymous": false,
          "createDateTime": "datetime",
          "author": {
            "userId": "uuid",
            "nickName": "string",
            "avatar": "string"
          }
        }
      ]
    }
  ],
  "pageInfo": {
    "size": 6,
    "count": 10,
    "current": 1
  }
}
```

---

### GET /api/movies/details/{id}
Получить детальную информацию о фильме.

**Параметры:**
- `id` (path, UUID): ID фильма

**Ответ (200):**
```json
{
  "id": "uuid",
  "name": "string",
  "poster": "string",
  "year": 2024,
  "country": "string",
  "genres": [...],
  "reviews": [...],
  "time": 120,
  "tagline": "string",
  "description": "string",
  "director": "string",
  "budget": 1000000,
  "fees": 5000000,
  "ageLimit": 16
}
```

**Ошибки:**
- 404: Фильм не найден

---

## Избранное

### GET /api/favorites/
Получить список избранных фильмов. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Ответ (200):**
```json
{
  "movies": [...]
}
```

**Ошибки:**
- 401: Не авторизован

---

### POST /api/favorites/{id}/add
Добавить фильм в избранное. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Параметры:**
- `id` (path, UUID): ID фильма

**Ответ (200):**
```json
{
  "message": "Movie added to favorites"
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Фильм не найден
- 409: Фильм уже в избранном

---

### DELETE /api/favorites/{id}/delete
Удалить фильм из избранного. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Параметры:**
- `id` (path, UUID): ID фильма

**Ответ (200):**
```json
{
  "message": "Movie removed from favorites"
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Фильм не найден в избранном

---

## Отзывы

### POST /api/movie/{movieId}/review/add
Добавить отзыв на фильм. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Параметры:**
- `movieId` (path, UUID): ID фильма

**Тело запроса:**
```json
{
  "reviewText": "string",
  "rating": 8,
  "isAnonymous": false
}
```

**Валидация:**
- `rating`: от 0 до 10
- `reviewText`: не пустая строка
- Один пользователь может оставить только один отзыв на фильм

**Ответ (200):**
```json
{
  "message": "Review added successfully"
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Фильм не найден
- 409: Вы уже оставили отзыв на этот фильм

---

### PUT /api/movie/{movieId}/review/{id}/edit
Редактировать отзыв. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Параметры:**
- `movieId` (path, UUID): ID фильма
- `id` (path, UUID): ID отзыва

**Тело запроса:**
```json
{
  "reviewText": "string",
  "rating": 9,
  "isAnonymous": false
}
```

**Ответ (200):**
```json
{
  "message": "Review updated successfully"
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Отзыв не найден
- 403: Вы можете редактировать только свои отзывы

---

### DELETE /api/movie/{movieId}/review/{id}/delete
Удалить отзыв. **Требует авторизации.**

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
```

**Параметры:**
- `movieId` (path, UUID): ID фильма
- `id` (path, UUID): ID отзыва

**Ответ (200):**
```json
{
  "message": "Review deleted successfully"
}
```

**Ошибки:**
- 401: Не авторизован
- 404: Отзыв не найден
- 403: Вы можете удалять только свои отзывы

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 200 | OK - Успешный запрос |
| 400 | Bad Request - Невалидные данные |
| 401 | Unauthorized - Не авторизован |
| 403 | Forbidden - Нет прав доступа |
| 404 | Not Found - Ресурс не найден |
| 409 | Conflict - Конфликт (дубликат) |
| 500 | Internal Server Error - Ошибка сервера |

---

## Примеры использования

### Полный цикл работы

1. **Регистрация:**
```bash
curl -X POST "http://localhost:8000/api/account/register" \
  -H "Content-Type: application/json" \
  -d '{"userName":"john","name":"John Doe","password":"secret123","email":"john@example.com","gender":0}'
```

2. **Сохранить токен из ответа**

3. **Получить список фильмов:**
```bash
curl "http://localhost:8000/api/movies/1"
```

4. **Добавить отзыв:**
```bash
curl -X POST "http://localhost:8000/api/movie/{MOVIE_ID}/review/add" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reviewText":"Amazing movie!","rating":10,"isAnonymous":false}'
```

5. **Добавить в избранное:**
```bash
curl -X POST "http://localhost:8000/api/favorites/{MOVIE_ID}/add" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

6. **Получить профиль:**
```bash
curl "http://localhost:8000/api/account/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Swagger UI

Для интерактивного тестирования API используйте Swagger UI:
http://localhost:8000/swagger

Swagger автоматически генерирует документацию и позволяет тестировать все endpoints прямо в браузере.

