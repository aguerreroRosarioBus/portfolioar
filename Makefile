.PHONY: help install test lint format clean docker-build docker-run docker-stop migrate makemigrations createsuperuser runserver collectstatic

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pip install pytest pytest-django flake8 black isort mypy django-stubs

test: ## Run tests
	python manage.py test

lint: ## Run linting
	flake8 .
	black --check .
	isort --check-only .
	mypy .

format: ## Format code
	black .
	isort .

clean: ## Clean up
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf staticfiles
	rm -rf media

docker-build: ## Build Docker image
	docker-compose build

docker-run: ## Run Docker containers
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

migrate: ## Run migrations
	python manage.py migrate

makemigrations: ## Make migrations
	python manage.py makemigrations

createsuperuser: ## Create superuser
	python manage.py createsuperuser

runserver: ## Run development server
	python manage.py runserver

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

shell: ## Open Django shell
	python manage.py shell

dbshell: ## Open database shell
	python manage.py dbshell

check: ## Run Django system checks
	python manage.py check

deploy: ## Deploy to production
	@echo "Deployment steps:"
	@echo "1. Run: make clean"
	@echo "2. Run: make install"
	@echo "3. Run: make migrate"
	@echo "4. Run: make collectstatic"
	@echo "5. Run: make test"
	@echo "6. Deploy using Docker or your preferred method"