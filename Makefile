.PHONY: help install dev build up down logs clean migrate migrate-up migrate-down migrate-revision test lint format

# Default target
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development
install: ## Install dependencies
	uv sync

dev: ## Start development server
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Docker
build: ## Build Docker images
	docker compose -f infrastructure/docker-compose.yaml build --no-cache

up: ## Start all services
	docker compose -f infrastructure/docker-compose.yaml up -d

down: ## Stop all services
	docker compose -f infrastructure/docker-compose.yaml down

logs: ## Show logs
	docker compose -f infrastructure/docker-compose.yaml logs -f

clean: ## Clean up Docker resources
	docker compose -f infrastructure/docker-compose.yaml down -v --remove-orphans
	docker system prune -f

# Database migrations (Docker)
migrate: ## Create new migration (usage: make migrate name=migration_name)
	docker compose -f infrastructure/docker-compose.yaml exec app alembic revision --autogenerate -m "$(name)"

migrate-up: ## Apply all migrations
	docker compose -f infrastructure/docker-compose.yaml exec app alembic upgrade head

migrate-down: ## Rollback last migration
	docker compose -f infrastructure/docker-compose.yaml exec app alembic downgrade -1

migrate-revision: ## Create empty migration (usage: make migrate-revision name=migration_name)
	docker compose -f infrastructure/docker-compose.yaml exec app alembic revision -m "$(name)"

# Local migrations (for development)
migrate-local: ## Create new migration locally (usage: make migrate-local name=migration_name)
	uv run alembic revision --autogenerate -m "$(name)"

migrate-up-local: ## Apply all migrations locally
	uv run alembic upgrade head

# Testing
test: ## Run tests
	uv run pytest

# Code quality
lint: ## Run linting
	uv run ruff check .

format: ## Format code
	uv run ruff format .

# Database
db-shell: ## Connect to database shell
	docker compose -f infrastructure/docker-compose.yaml exec db psql -U shortener -d shortener

# Quick start
start: build up ## Build, start services and apply migrations
	@echo "🚀 Application started! Visit http://localhost:8000"

# Development setup
setup: install build up migrate-up ## Full development setup
	@echo "✅ Development environment ready!"
	@echo "📊 API docs: http://localhost:8000/docs"
	@echo "🔍 Health check: http://localhost:8000/health" 