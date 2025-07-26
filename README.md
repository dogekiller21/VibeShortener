# Vibe Shortener

Быстрый URL-шортенер с метриками, построенный на FastAPI и PostgreSQL.

## Особенности

- ⚡ **Быстрый**: FastAPI + PostgreSQL с оптимизированными настройками
- 📊 **Метрики**: Отслеживание переходов, IP, User-Agent, Referer
- 🐳 **Docker**: Полная инфраструктура в контейнерах
- 🔧 **Миграции**: Alembic для управления схемой БД
- 🎯 **Простой API**: Создание ссылок и просмотр статистики

## API Endpoints

### Создание короткой ссылки
```bash
POST /shorten
Content-Type: application/json

{
  "original_url": "https://example.com/very-long-url"
}
```

### Переход по короткой ссылке
```bash
GET /{short_code}
# Автоматический редирект на оригинальный URL
```

### Статистика по ссылке
```bash
GET /stats/{short_code}
```

### Проверка здоровья
```bash
GET /health
```

## Быстрый старт (локальная разработка)

1. Установить зависимости:
   ```bash
   make install
   ```
2. Применить миграции (локально):
   ```bash
   make migrate-up-local
   ```
3. Запустить dev-сервер (hot-reload):
   ```bash
   make dev
   ```

## Быстрый старт (через Docker/self-hosting)

1. Собрать образы:
   ```bash
   make build
   ```
2. Запустить сервисы (backend + база):
   ```bash
   make up
   ```
3. Применить миграции (в контейнере):
   ```bash
   make migrate-up
   ```
4. Остановить сервисы:
   ```bash
   make down
   ```

## Полный цикл (одной командой)

- Через Docker:
  ```bash
  make start
  ```
- Локально:
  ```bash
  make setup
  ```

## Открыть API:
```
http://localhost:8000/docs
```

---

## Self-Hosting

### Требования

- Docker и Docker Compose
- Git
- Минимум 1GB RAM
- 10GB свободного места

### Быстрое развертывание

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/vibe-shortener.git
cd vibe-shortener
```

2. **Настройте переменные окружения:**
```bash
# Создайте файлы с вашими настройками
cp infrastructure/env/backend.env.example infrastructure/env/backend.env
cp infrastructure/env/db.env.example infrastructure/env/db.env

# Отредактируйте файлы под ваше окружение
nano infrastructure/env/backend.env
nano infrastructure/env/db.env
```

3. **Запустите приложение:**
```bash
make start
```

### Продакшн настройки

#### Переменные окружения

**backend.env:**
```env
DATABASE_URL=postgresql://user:password@host:5432/database
ENVIRONMENT=production
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

#### Nginx конфигурация

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

#### SSL с Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Автозапуск

Создайте systemd сервис `/etc/systemd/system/vibe-shortener.service`:

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

Активируйте автозапуск:
```bash
sudo systemctl enable vibe-shortener
sudo systemctl start vibe-shortener
```

### Мониторинг

#### Логи
```bash
# Просмотр логов
make logs

# Логи конкретного сервиса
docker compose -f infrastructure/docker-compose.yml logs app
docker compose -f infrastructure/docker-compose.yml logs db
```

#### База данных
```bash
# Подключение к БД
make db-shell

# Резервное копирование
docker compose -f infrastructure/docker-compose.yml exec db pg_dump -U shortener shortener > backup.sql

# Восстановление
docker compose -f infrastructure/docker-compose.yml exec -T db psql -U shortener shortener < backup.sql
```

#### Метрики

Проверьте статистику в PostgreSQL:
```sql
-- Топ ссылок по переходам
SELECT u.short_code, u.original_url, COUNT(c.id) as clicks
FROM urls u
LEFT JOIN clicks c ON u.id = c.url_id
GROUP BY u.id, u.short_code, u.original_url
ORDER BY clicks DESC
LIMIT 10;
```

### Обновление

1. **Остановите сервисы:**
```bash
make down
```

2. **Обновите код:**
```bash
git pull origin main
```

3. **Пересоберите и запустите:**
```bash
make start
```

4. **Примените миграции (если есть):**
```bash
make migrate-up
```

### Безопасность

#### Рекомендации для продакшна:

1. **Измените пароли по умолчанию**
2. **Используйте HTTPS**
3. **Настройте firewall**
4. **Регулярно обновляйте зависимости**
5. **Мониторьте логи на подозрительную активность**

#### Firewall (Ubuntu/Debian):
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Структура проекта

```
vibe_shortener/
├── backend/
│   ├── src/              # FastAPI приложение
│   ├── alembic/          # Миграции БД
│   └── ...
├── web/                  # Будущий фронтенд
├── infrastructure/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── env/              # Переменные окружения
├── README.md
└── Makefile
```

## Настройки

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://shortener:shortener@localhost:5432/shortener
ENVIRONMENT=development
DOMAIN=localhost:8000
```

## Разработка

### Установка dev-зависимостей:
```bash
make install
```

### Линтинг:
```bash
make lint
make format
```

### Тесты:
```bash
make test
```

## Производительность

### Оптимизации PostgreSQL:
- Connection pooling (10-30 соединений)
- Индексы на ключевых полях
- Оптимизированные настройки для URL-шортенера
- pg_stat_statements для мониторинга

### Оптимизации FastAPI:
- Асинхронные эндпоинты
- Множественные воркеры (4 по умолчанию)
- Валидация через Pydantic

## Мониторинг

### Health Check:
```bash
curl http://localhost:8000/health
```

### Статистика PostgreSQL:
```sql
-- Топ ссылок по переходам
SELECT u.short_code, u.original_url, COUNT(c.id) as clicks
FROM urls u
LEFT JOIN clicks c ON u.id = c.url_id
GROUP BY u.id, u.short_code, u.original_url
ORDER BY clicks DESC
LIMIT 10;
```

## Деплой

### Docker Compose (продакшн):
```bash
make start
```

### Переменные окружения для продакшна:
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
ENVIRONMENT=production
DOMAIN=your-domain.com
```

## Лицензия

MIT
