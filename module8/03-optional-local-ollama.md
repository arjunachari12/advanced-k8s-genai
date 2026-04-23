# Exercise 3: Optional Local Ollama Backend

Use this exercise if you want to keep inference local instead of using a hosted provider.

## What You Are Building

You are running a small OpenAI-compatible bridge in front of Ollama so tools that expect an OpenAI-style API can talk to a local model.

This is useful for:

- privacy-sensitive experimentation
- offline or lab-only demos
- understanding how thin compatibility layers can connect tools together

## Step 1: Validate the Compose File

```bash
docker compose -f module8/local-mcp-ollama/docker-compose.yaml config
```

## Step 2: Start the Local Services

```bash
cd module8/local-mcp-ollama
docker compose up -d --build
```

This starts:

- an `ollama` container
- a lightweight compatibility server on port `8888`

## Step 3: Point kubectl-ai at the Local Bridge

```bash
export KUBECTL_AI_PROVIDER="openai"
export OPENAI_API_BASE="http://localhost:8888/v1"
export OPENAI_API_KEY="local"
```

## Step 4: Test a Prompt

```bash
kubectl ai "explain what a Kubernetes service does"
```

If the response is empty or slow, check whether Ollama has a model available and whether the containers are healthy.

## Verify the Environment

```bash
docker compose ps
docker compose logs --tail=50
```

## Cleanup

```bash
docker compose -f module8/local-mcp-ollama/docker-compose.yaml down -v
```

## What Just Happened?

You replaced a hosted LLM endpoint with a local one while keeping an OpenAI-compatible interface. This shows students that AI tooling is often just a thin layer around model APIs, and that those backends can be swapped when the interface stays stable.
