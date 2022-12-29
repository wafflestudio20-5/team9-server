.PHONY: local server

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(lastword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-local: ## Run local server
	./run_api.sh

down-local: ## Shut down local server
	pkill -f gunicorn