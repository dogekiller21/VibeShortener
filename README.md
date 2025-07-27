# Vibe Shortener

🚀 **Современный URL-шортенер с детальной аналитикой и геолокацией**

Быстрый и удобный сервис для создания коротких ссылок с продвинутой статистикой переходов, построенный на FastAPI, PostgreSQL и современном веб-интерфейсе.

## ✨ Особенности

- ⚡ **Быстрый**: FastAPI + PostgreSQL с оптимизированными настройками
- 📊 **Детальная аналитика**: Статистика переходов, геолокация, графики активности
- 🌍 **Геолокация**: Отслеживание IP-адресов с определением страны, региона и города
- 🎨 **Современный UI**: Адаптивный дизайн с Tailwind CSS и интерактивными графиками
- 💾 **Локальное хранение**: Автоматическое сохранение ссылок в браузере
- 🔧 **Миграции**: Alembic для управления схемой БД
- 🐳 **Docker**: Полная инфраструктура в контейнерах
- 🎯 **Простой API**: RESTful API с автоматической документацией

## 🏗️ Архитектура

### Технологический стек
- **Backend**: FastAPI 0.116+ (Python 3.13)
- **Database**: PostgreSQL 16 с оптимизациями
- **ORM**: SQLAlchemy 2.0 (асинхронный, современный синтаксис)
- **Validation**: Pydantic v2
- **Frontend**: Jinja2 + Tailwind CSS + Chart.js
- **Geolocation**: Множественные API (ip-api.com, ipinfo.io)
- **Package Manager**: uv
- **Linting**: Ruff

### Структура проекта
```
vibe_shortener/
├── src/                    # Основной код приложения
│   ├── main.py            # FastAPI приложение
│   ├── config.py          # Pydantic Settings
│   ├── database.py        # Async SQLAlchemy
│   ├── models.py          # SQLAlchemy модели
│   ├── schemas.py         # Pydantic схемы + DTOs
│   ├── services.py        # Бизнес-логика с DTO
│   ├── geolocation.py     # Сервис геолокации
│   ├── utils.py           # Утилиты
│   ├── routes/            # API маршруты
│   │   ├── shortener.py   # Создание ссылок
│   │   ├── redirect.py    # Редиректы
│   │   ├── stats.py       # Статистика
│   │   └── health.py      # Health check
│   └── web/               # Веб-интерфейс
│       ├── templates/     # Jinja2 шаблоны
│       └── static/        # Статические файлы
├── infrastructure/         # Docker инфраструктура
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   └── env/               # Переменные окружения
├── alembic/               # Миграции БД
├── pyproject.toml         # Зависимости (uv)
├── Makefile               # Команды разработки
└── README.md
```

## 🚀 Быстрый старт

### Локальная разработка (рекомендуется)

1. **Установить зависимости:**
   ```bash
   make install
   ```

2. **Настроить базу данных:**
   ```bash
   # Запустить PostgreSQL локально или через Docker
   docker run -d --name postgres-shortener \
     -e POSTGRES_DB=shortener \
     -e POSTGRES_USER=shortener \
     -e POSTGRES_PASSWORD=shortener \
     -p 5432:5432 \
     postgres:16-alpine
   ```

3. **Применить миграции:**
   ```bash
   make migrate-up-local
   ```

4. **Запустить dev-сервер:**
   ```bash
   make dev
   ```

5. **Открыть приложение:**
   ```
   http://localhost:8000
   ```

### Docker Compose (self-hosting)

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com/your-username/vibe-shortener.git
   cd vibe-shortener
   ```

2. **Настроить переменные окружения:**
   ```bash
   cp infrastructure/env/backend.env.example infrastructure/env/backend.env
   cp infrastructure/env/db.env.example infrastructure/env/db.env
   # Отредактировать файлы под ваше окружение
   ```

3. **Запустить все сервисы:**
   ```bash
   make start
   ```

4. **Открыть приложение:**
   ```
   http://localhost:8000
   ```

## 📊 API Endpoints

### Создание короткой ссылки
```bash
POST /api/v1/shorten
Content-Type: application/json

{
  "original_url": "https://example.com/very-long-url"
}
```

**Ответ:**
```json
{
  "id": 1,
  "original_url": "https://example.com/very-long-url",
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Переход по короткой ссылке
```bash
GET /{short_code}
# Автоматический редирект на оригинальный URL
# + запись метрик (IP, User-Agent, Referer, геолокация)
```

### Базовая статистика
```bash
GET /api/v1/stats/{short_code}
```

**Ответ:**
```json
{
  "url_id": 1,
  "short_code": "abc123",
  "original_url": "https://example.com/very-long-url",
  "short_url": "http://localhost:8000/abc123",
  "total_clicks": 42,
  "created_at": "2024-01-01T12:00:00Z",
  "last_click": "2024-01-15T14:30:00Z"
}
```

### Детальная статистика с графиками
```bash
GET /api/v1/stats/{short_code}/detailed
```

**Ответ включает:**
- График активности за 7 дней
- Распределение переходов по часам
- Топ User-Agent'ов
- Географию переходов с координатами

### Проверка здоровья
```bash
GET /health
```

## 🌐 Веб-интерфейс

### Главная страница (`/`)
- Создание коротких ссылок
- Автоматическое сохранение в localStorage
- Копирование ссылок в буфер обмена

### Мои ссылки (`/links`)
- Просмотр всех сохраненных ссылок
- Поиск по ссылкам
- Обновление статистики
- Быстрый доступ к детальной статистике

### Статистика (`/stats`)
- Детальная аналитика с графиками
- Географическая визуализация
- Интерактивные диаграммы (Chart.js)
- Тепловая карта переходов

## 🔧 Конфигурация

### Переменные окружения

**backend.env:**
```env
DATABASE_URL=postgresql://user:password@host:5432/database
ENVIRONMENT=production  # development/production
DOMAIN=your-domain.com
```

**db.env:**
```env
POSTGRES_DB=shortener
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Оптимизации PostgreSQL
- Connection pooling (10-30 соединений)
- Индексы на ключевых полях
- pg_stat_statements для мониторинга
- Оптимизированные настройки для URL-шортенера

## 🛠️ Разработка

### Установка зависимостей
```bash
make install
```

### Линтинг и форматирование
```bash
make lint    # Проверка кода
make format  # Форматирование
```

### Тесты
```bash
make test
```

### Миграции
```bash
# Создать новую миграцию
make migrate-local name=add_new_field

# Применить миграции
make migrate-up-local

# Откатить последнюю миграцию
make migrate-down
```

### База данных
```bash
# Подключиться к БД
make db-shell

# Резервное копирование
docker compose -f infrastructure/docker-compose.yaml exec db pg_dump -U shortener shortener > backup.sql
```

## 🚀 Продакшн развертывание

### Требования
- Docker и Docker Compose
- Git
- Минимум 1GB RAM
- 10GB свободного места

### Быстрое развертывание

1. **Клонировать и настроить:**
   ```bash
   git clone https://github.com/your-username/vibe-shortener.git
   cd vibe-shortener
   
   # Настроить переменные окружения
   cp infrastructure/env/backend.env.example infrastructure/env/backend.env
   cp infrastructure/env/db.env.example infrastructure/env/db.env
   nano infrastructure/env/backend.env
   nano infrastructure/env/db.env
   ```

2. **Запустить:**
   ```bash
   make start
   ```

### Nginx конфигурация

Создайте файл `/etc/nginx/sites-available/vibe-shortener`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте сайт:
```bash
sudo ln -s /etc/nginx/sites-available/vibe-shortener /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL с Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Автозапуск (systemd)

Создайте `/etc/systemd/system/vibe-shortener.service`:

```ini
[Unit]
Description=Vibe Shortener
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/vibe-shortener
ExecStart=/usr/bin/docker compose -f infrastructure/docker-compose.yml up -d
ExecStop=/usr/bin/docker compose -f infrastructure/docker-compose.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Активируйте:
```bash
sudo systemctl enable vibe-shortener
sudo systemctl start vibe-shortener
```

## 📈 Мониторинг

### Логи
```bash
# Просмотр логов
make logs

# Логи конкретного сервиса
docker compose -f infrastructure/docker-compose.yml logs app
docker compose -f infrastructure/docker-compose.yml logs db
```

### Метрики PostgreSQL
```sql
-- Топ ссылок по переходам
SELECT u.short_code, u.original_url, COUNT(c.id) as clicks
FROM urls u
LEFT JOIN clicks c ON u.id = c.url_id
GROUP BY u.id, u.short_code, u.original_url
ORDER BY clicks DESC
LIMIT 10;

-- Статистика по географии
SELECT 
    c.ip_address,
    COUNT(*) as clicks,
    COUNT(DISTINCT c.url_id) as unique_urls
FROM clicks c
WHERE c.ip_address IS NOT NULL
GROUP BY c.ip_address
ORDER BY clicks DESC
LIMIT 20;

-- Активность по дням (последние 7 дней)
SELECT 
    DATE(created_at) as date,
    COUNT(*) as clicks
FROM clicks 
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date;

-- Распределение по часам
SELECT 
    EXTRACT(HOUR FROM created_at) as hour,
    COUNT(*) as clicks
FROM clicks 
GROUP BY EXTRACT(HOUR FROM created_at)
ORDER BY hour;
```

### Обновление
```bash
# Остановить сервисы
make down

# Обновить код
git pull origin main

# Пересобрать и запустить
make start

# Применить миграции (если есть)
make migrate-up
```

## 🔒 Безопасность

### Рекомендации для продакшна:
1. **Измените пароли по умолчанию**
2. **Используйте HTTPS**
3. **Настройте firewall**
4. **Регулярно обновляйте зависимости**
5. **Мониторьте логи на подозрительную активность**

### Firewall (Ubuntu/Debian):
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```



## 📝 Лицензия

MIT

---

**Vibe Shortener** - современный, быстрый и удобный сервис для создания коротких ссылок с продвинутой аналитикой. 🚀
