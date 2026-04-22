PYTHON ?= python3

.PHONY: validate validate-python validate-helm validate-compose clean-python-cache

validate: validate-python validate-helm validate-compose

validate-python:
	$(PYTHON) -m compileall module2 module8 module9

validate-helm:
	helm lint module5/chart
	helm template genai module5/chart --namespace genai-staging -f module5/chart/values-staging.yaml >/tmp/genai-module5-rendered.yaml

validate-compose:
	docker compose -f module2/docker-compose.yaml config >/tmp/module2-compose-config.yaml
	docker compose -f module8/local-mcp-ollama/docker-compose.yaml config >/tmp/module8-local-mcp-ollama-config.yaml

clean-python-cache:
	find module2 module8 module9 -type d -name '__pycache__' -prune -exec rm -rf {} +
	find module2 module8 module9 -type f -name '*.pyc' -delete
