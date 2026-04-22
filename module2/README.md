# Module 2: Manual Deployment with Kubernetes YAML

Module 2 introduces the core GenAI application and deploys it with plain Kubernetes manifests before Helm or GitOps are introduced.

## What Students Build

A small three-service application:

- `ui` - static web frontend
- `api` - FastAPI backend
- `llm` - local Ollama runtime

Request flow:

`Browser -> UI -> API -> Ollama`

## Learning Objectives

1. build container images for a small GenAI platform
2. deploy the app with raw Kubernetes YAML
3. understand the relationship between Deployments, Services, PVCs, and Ingress
4. validate the app end to end

## Architecture / Flow

- The UI serves a static form and proxies `/api` traffic.
- The API builds prompts and calls Ollama over HTTP.
- Ollama serves a local `tinyllama` model.

## Assets In This Module

- `ui/` - frontend container
- `api/` - FastAPI application with `/generate`, `/health`, and `/metrics`
- `llm/` - Ollama container setup
- `k8s/` - namespace, deployments, services, and ingress
- `docker-compose.yaml` - local non-Kubernetes smoke test

## Prerequisites

- Module 1 completed
- Docker working locally
- a running KIND cluster

## Step 1: Review the App Structure

Key files to review:

- `api/app/main.py`
- `ui/index.html`
- `llm/entrypoint.sh`

## Step 2: Build the Images

The manifests in this module already reference published images, but students can rebuild locally to understand the container flow:

```bash
cd module2

docker build -t arjunachari12/genai-ui:1.0.1 ./ui
docker build -t arjunachari12/genai-api:1.0.0 ./api
docker build -t arjunachari12/genai-ollama:1.0.0 ./llm
```

If you want to use only local KIND images instead of pulling from a registry, retag them and load them into KIND:

```bash
kind load docker-image arjunachari12/genai-ui:1.0.1 --name multi-node-cluster
kind load docker-image arjunachari12/genai-api:1.0.0 --name multi-node-cluster
kind load docker-image arjunachari12/genai-ollama:1.0.0 --name multi-node-cluster
```

## Step 3: Apply the Kubernetes Manifests

```bash
kubectl apply -f k8s/namespaces.yaml
kubectl apply -f k8s/llm-deployment.yaml
kubectl apply -f k8s/llm-service.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/api-service.yaml
kubectl apply -f k8s/ui-deployment.yaml
kubectl apply -f k8s/ui-service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Step 4: Validate the Workload

```bash
kubectl get pods -n genai
kubectl get svc -n genai
kubectl get ingress -n genai
```

Expected result:

- `ui`, `api`, and `llm` pods become `Running`
- services are present for each component

## Step 5: Access the UI

Port-forward the frontend:

```bash
kubectl -n genai port-forward svc/ui-service 8080:80
```

Open:

```text
http://127.0.0.1:8080
```

## Step 6: Test the End-to-End Path

```bash
curl http://127.0.0.1:8080/healthz

curl -X POST http://127.0.0.1:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "product": "AI-powered coffee subscription",
    "audience": "busy engineering managers"
  }'
```

Students should observe:

- the UI can reach the API
- the API can reach Ollama
- the JSON response includes `model`, `prompt`, and `content`

## Optional: Local Smoke Test With Docker Compose

```bash
cd module2
docker compose up --build
```

Then open `http://localhost:8080`.

If you want to validate the Compose file without starting containers:

```bash
docker compose config
```

## Troubleshooting

- If the `llm` pod stays unready, give Ollama more time to pull the model on first start.
- If `http://127.0.0.1:8080` does not work, confirm the `kubectl port-forward` terminal is still running.
- If the API returns timeouts, inspect `kubectl logs -n genai deploy/api` and `kubectl logs -n genai deploy/llm`.

## Cleanup

```bash
kubectl delete namespace genai --ignore-not-found
docker compose down -v || true
```

## Instructor Validation Checklist

- `kubectl get pods -n genai` shows all application pods running
- the UI loads through port-forward
- `POST /api/generate` returns JSON with model output

## Exit Criteria

Students are ready for Module 3 when:

- the app is reachable through the UI
- `POST /api/generate` succeeds
- they understand which YAML file creates each Kubernetes resource
