# Context & User Preferences

## Python Version & Syntax
- **Python 3.13** - используем современный синтаксис
- **Union types**: `str | None` вместо `Optional[str]`
- **No Optional imports** - не импортируем `Optional` из `typing`

## Pydantic v2
- **Config class deprecated** - используем `model_config = ConfigDict(from_attributes=True)`
- **dict() deprecated** - используем `model_dump()` вместо `dict()`

## SQLAlchemy 2.0
- **mapped_column** вместо `Column`
- **AsyncSession** для асинхронных операций
- **select()** вместо `.query()`
- **scalar_one_or_none()** для получения одного результата

## DateTime
- **datetime.utcnow() deprecated** - используем `datetime.now(timezone.utc)`
- **server_default** для SQL-операций: `func.timezone('UTC', func.now())`

## Docker Compose & Dockerfile
- **version deprecated** - не указываем версию в docker-compose.yml
- **Infrastructure в отдельной папке** - все Docker файлы в `infrastructure/`
- **EXPOSE, HEALTHCHECK, CMD** — только в docker-compose, не в Dockerfile. Dockerfile — только для build.

## Code Quality
- **Ruff** вместо mypy для линтинга
- **uv** для управления зависимостями
- **Актуальные версии** пакетов

## Architecture Preferences
- **DTO для сервисов** - сервисы возвращают структурированные DTO (URLDTO, ClickDTO, URLStatsDTO), не сырые SQLAlchemy объекты
- **Избегаем detached objects** - никогда не возвращаем SQLAlchemy объекты из сервисов
- **Асинхронность** - везде где возможно используем async/await
- **Типобезопасность** - везде указываем типы

## Error Handling
- **Защита от вечных циклов** - ограничения на retry (например, 100 попыток)
- **Graceful degradation** - возвращаем None и обрабатываем в контроллере

## Database
- **PostgreSQL** с оптимизациями для URL shortener
- **Alembic** для миграций
- **Индексы** через `index=True` в mapped_column

## FastAPI
- **Асинхронные эндпоинты**
- **Pydantic для валидации**
- **Структурированные ответы**

## Frontend & Templates
- **Jinja2 шаблоны** с базовым шаблоном `base.html`
- **Tailwind CSS** для стилизации
- **Адаптивный дизайн** - мобильная и десктопная версии
- **Анимации** - плавные переходы и эффекты
- **UX/UI** - современный интерфейс с шапкой и футером

## Project Structure
```
src/
├── config.py      # Pydantic Settings
├── database.py    # Async SQLAlchemy
├── models.py      # SQLAlchemy models с mapped_column
├── schemas.py     # Pydantic schemas + DTOs
├── services.py    # Business logic с DTO
├── main.py        # FastAPI app
└── web/
    └── templates/
        ├── base.html      # Базовый шаблон с шапкой/футером
        ├── index.html     # Главная страница
        └── stats.html     # Страница статистики

infrastructure/
├── docker-compose.yml  # Без version
├── Dockerfile
└── postgres/
    └── init.sql
```

## Key Rules
1. Всегда используй Python 3.13 синтаксис
2. Никогда не используй deprecated методы
3. Сервисы возвращают DTO, не SQLAlchemy объекты
4. Всегда асинхронные операции с БД
5. Защищай от вечных циклов
6. Инфраструктура в отдельной папке
7. EXPOSE, HEALTHCHECK, CMD — только в docker-compose, не в Dockerfile
8. Используй базовый шаблон для всех страниц
9. Современный UI с адаптивным дизайном 