.PHONY: up down build rebuild shell web-shell db-shell logs test migrate run

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

rebuild:
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d

shell:
	docker-compose exec web bash

web-shell:
	docker-compose exec web python manage.py shell

db-shell:
	docker-compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

logs:
	docker-compose logs -f

test:
	docker-compose exec web python manage.py test

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --no-input
