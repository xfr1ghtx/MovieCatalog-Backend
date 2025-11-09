# Настройка переменных окружения

## Быстрая настройка

### Для Docker (рекомендуется)
```bash
# Переменные окружения для Docker уже настроены в docker-compose.yml
# Просто запустите:
docker-compose up -d
```

### Для локальной разработки

1. **Скопируйте файл .env.example**
```bash
cp .env.example .env
```

2. **Отредактируйте .env файл**
```bash
# Используйте любой текстовый редактор
nano .env
# или
code .env
```

3. **Обязательно измените JWT_SECRET_KEY**
```bash
# Сгенерируйте случайный ключ:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Или используйте:
openssl rand -hex 32
```

---

## Описание переменных

### 🔐 Обязательные переменные

#### DATABASE_URL
URL для подключения к PostgreSQL базе данных.

**Формат:**
```
postgresql://username:password@host:port/database_name
```

**Примеры:**
```bash
# Локальная БД
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movie_catalog

# Docker (внутри контейнера)
DATABASE_URL=postgresql://postgres:postgres@db:5432/movie_catalog

# Внешний сервер
DATABASE_URL=postgresql://user:pass@db.example.com:5432/moviedb
```

#### JWT_SECRET_KEY
Секретный ключ для подписи JWT токенов. **ОЧЕНЬ ВАЖНО**: Измените это значение в production!

**Генерация:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Пример:**
```bash
JWT_SECRET_KEY=xK8h_9mP3nQ7rT2vW5yZ4aB6cD1eF0gH3jI9kL2mN8oP4qR7sT1uV6wX3yZ9
```

⚠️ **ВНИМАНИЕ**: Никогда не коммитьте реальный ключ в git!

#### JWT_ALGORITHM
Алгоритм шифрования для JWT.

**Значение по умолчанию:**
```bash
JWT_ALGORITHM=HS256
```

**Возможные значения:** HS256, HS384, HS512, RS256, RS384, RS512

### ⏱️ Время жизни токенов

#### ACCESS_TOKEN_EXPIRE_MINUTES
Время жизни access токена в минутах.

**Рекомендации:**
- Разработка: 30-60 минут
- Production: 15-30 минут
- Для mobile apps: 60-120 минут

```bash
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### REFRESH_TOKEN_EXPIRE_DAYS
Время жизни refresh токена в днях.

**Рекомендации:**
- Разработка: 7 дней
- Production: 7-30 дней

```bash
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 🌐 API настройки

#### API_V1_PREFIX
Префикс для всех API endpoints.

```bash
API_V1_PREFIX=/api
```

Результат: все endpoints будут доступны по `/api/*`

#### PROJECT_NAME
Название проекта (отображается в Swagger UI).

```bash
PROJECT_NAME=MovieCatalog.API
```

### 🔓 CORS настройки

#### BACKEND_CORS_ORIGINS
Список разрешенных origins для CORS запросов (в формате JSON).

**Формат:**
```bash
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080","https://example.com"]
```

**Важно:**
- Используйте правильный JSON формат (двойные кавычки)
- Для разработки: включите localhost порты вашего фронтенда
- Для production: указывайте только реальные домены

**Примеры:**
```bash
# Development
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]

# Production
BACKEND_CORS_ORIGINS=["https://myapp.com","https://www.myapp.com"]

# Разрешить все (НЕ ИСПОЛЬЗУЙТЕ в production!)
BACKEND_CORS_ORIGINS=["*"]
```

---

## 📋 Примеры конфигураций

### Development (локальная разработка)
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movie_catalog
JWT_SECRET_KEY=dev-secret-key-DO-NOT-USE-IN-PRODUCTION
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_PREFIX=/api
PROJECT_NAME=MovieCatalog.API [DEV]
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

### Production
```bash
DATABASE_URL=postgresql://produser:strongpassword@db.example.com:5432/moviedb
JWT_SECRET_KEY=xK8h_9mP3nQ7rT2vW5yZ4aB6cD1eF0gH3jI9kL2mN8oP4qR7sT1uV6wX3yZ9
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
API_V1_PREFIX=/api
PROJECT_NAME=MovieCatalog.API
BACKEND_CORS_ORIGINS=["https://myapp.com","https://www.myapp.com"]
DEBUG=False
```

### Docker Compose (docker-compose.yml)
```yaml
environment:
  DATABASE_URL: postgresql://postgres:postgres@db:5432/movie_catalog
  JWT_SECRET_KEY: ${JWT_SECRET_KEY:-your-secret-key}
  JWT_ALGORITHM: HS256
  ACCESS_TOKEN_EXPIRE_MINUTES: 30
  REFRESH_TOKEN_EXPIRE_DAYS: 7
```

---

## 🔒 Безопасность

### ✅ Лучшие практики

1. **Никогда не коммитьте .env файл**
   - `.env` уже в `.gitignore`
   - Коммитьте только `.env.example`

2. **Используйте сложный JWT_SECRET_KEY**
   - Минимум 32 символа
   - Случайные символы
   - Разный ключ для каждого окружения

3. **Разные настройки для dev/prod**
   - Development: более длительные токены, отладка включена
   - Production: короткие токены, отладка выключена

4. **Используйте переменные окружения на сервере**
   - Не храните секреты в файлах
   - Используйте секреты в CI/CD (GitHub Secrets, GitLab CI/CD Variables)
   - Используйте vault системы (HashiCorp Vault, AWS Secrets Manager)

### ⚠️ Что НЕ делать

❌ Не коммитьте `.env` в git  
❌ Не используйте простые ключи типа "secret" или "password"  
❌ Не используйте одинаковый `JWT_SECRET_KEY` для dev и prod  
❌ Не делитесь `.env` файлом через мессенджеры  
❌ Не храните production секреты в открытом виде

---

## 🚀 Быстрый старт

### Docker (проще всего)
```bash
# Всё уже настроено в docker-compose.yml
docker-compose up -d
```

### Локальная разработка
```bash
# 1. Создайте .env
cp .env.example .env

# 2. Сгенерируйте JWT ключ
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# 3. Добавьте ключ в .env файл
# Откройте .env и замените JWT_SECRET_KEY

# 4. Запустите приложение
uvicorn app.main:app --reload
```

---

## 🐛 Решение проблем

### Ошибка подключения к БД
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Решение:**
1. Проверьте, что PostgreSQL запущен
2. Проверьте правильность `DATABASE_URL`
3. Для Docker: используйте `db` вместо `localhost` в URL

### Ошибка JWT токена
```
jose.exceptions.JWTError: Invalid crypto padding
```

**Решение:**
1. Проверьте, что `JWT_SECRET_KEY` установлен
2. Убедитесь, что ключ не содержит специальных символов
3. Сгенерируйте новый ключ

### CORS ошибка
```
Access to fetch at ... from origin ... has been blocked by CORS policy
```

**Решение:**
1. Добавьте origin фронтенда в `BACKEND_CORS_ORIGINS`
2. Проверьте формат JSON (двойные кавычки)
3. Перезапустите API после изменения

---

## 📞 Дополнительная помощь

- Смотрите [README.md](README.md) для общей документации
- Смотрите [QUICKSTART.md](QUICKSTART.md) для быстрого старта
- Проверьте [docker-compose.yml](docker-compose.yml) для примера конфигурации

---

**Важно**: Всегда храните production секреты в безопасном месте и никогда не коммитьте их в систему контроля версий!

