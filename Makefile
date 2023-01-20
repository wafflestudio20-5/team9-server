.PHONY: local server

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(lastword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

test: ## Run test code
	cd ./dear_j && python manage.py test

run-local: ## Run local server (127.0.0.1:8000)
	cd ./dear_j && python manage.py runserver

run-dev: ## Run dev server
	export SITE=DEV && ./scripts/run-local.sh

down-dev: ## Shut down dev server
	pkill -f gunicorn

run-dev-with-docker: ## Run dev container
	docker-compose down && docker-compose up --build -d

down-dev-with-docker: ## Shut down dev container
	docker-compose down
