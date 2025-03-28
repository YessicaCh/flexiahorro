#!make
.DEFAULT_GOAL :=help
.PHONY:  help test ps stop build collectstatic up down makemigrations migrate logs bash shell update upgrade runserver

include .env
export $(shell sed 's/=.*//' .env)

ps: ## list docker processes: make ps
	@docker ps --no-trunc

pull: ## build pull: make pull
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) --verbose pull

stop: ## detener todos contenedores: make stop
	@docker stop $(docker ps -a -q)

build: ## build sandbox: make build-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) --verbose build

collectstatic: ## static sandbox: make static-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run --rm web python manage.py collectstatic --noinput

db: ## run sandbox: make up-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) up db
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) ps

up: ## run sandbox: make up-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) --verbose up -d --force-recreate
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) ps

down: ## run sandbox: make down-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) down
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) ps

makemigrations: ## migrate: make migrate-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run --rm web python manage.py makemigrations

runserver: ## migrate: make migrate-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run web python manage.py runserver

migrate: ## migrate: make migrate-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run --rm web python manage.py migrate

tts: ## migrate: make migrate-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run --rm web python manage.py tts_story --last_stories True

logs: ## migrate: make migrate-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker logs -f $(SITE)-$(ENV)-web

bash: ## exec bash: make bash-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker exec -it $(SITE)-$(ENV)-web bash

bash-cron: ## exec bash: make bash-sandbox
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker exec -it $(SITE)-$(ENV)-cron bash

shell: ## exec bash: make bash-prod
	ENV=$(ENV) \
	SITE=$(SITE) \
	DB_PORT=$(DB_PORT) \
	CACHE_PORT=$(CACHE_PORT) \
	WEB_PORT=$(WEB_PORT) \
	docker-compose -f docker-compose.${DOCKER_ENVIRONMENT}.yml -p $(SITE)_$(ENV) run --rm web python manage.py shell_plus

update: ## update project: make update
	@git pull
	@make migrate
	@make collectstatic
	@make up

upgrade: ## upgrade project whit migrations: make upgrade
	@make down
	@git pull
	@make build
	@make migrate
	@make collectstatic
	@make up

## HELP TARGET ##
help:
	@echo $(SITE)
	@printf "\033[31m%-22s %-59s %s\033[0m\n" " Target " "  Help  " "  Usage  "; \
	printf "\033[31m%-22s %-59s %s\033[0m\n"  "--------" "--------" "---------"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-22s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
