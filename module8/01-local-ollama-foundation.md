# Exercise 1: Run a Local Ollama Backend for Classroom Demos

Start here if you want Module 8 to work even when students do not have an OpenAI or Gemini API key.

## What You Are Building

You are running a small OpenAI-compatible bridge in front of Ollama so tools that expect an OpenAI-style API can talk to a local model.

This is useful for:

- privacy-sensitive experimentation
- offline or lab-only demos
- understanding how thin compatibility layers can connect tools together

This first exercise creates the local AI endpoint that the next exercise can reuse with `kubectl-ai`.

## Prerequisites

- `kubectl` works against your cluster
- internet access is available for plugin installation
- you have an LLM provider key, such as `OPENAI_API_KEY` or `GEMINI_API_KEY`

## Install Krew If Needed

```bash
(
  set -x
  cd "$(mktemp -d)"
  OS="$(uname | tr '[:upper:]' '[:lower:]')"
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
  KREW="krew-${OS}_${ARCH}"
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz"
  tar zxvf "${KREW}.tar.gz"
  ./"${KREW}" install krew
)
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
```

## Install kubectl-ai

```bash
kubectl krew install ai
```

Verify:

```bash
kubectl ai --help
```


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

On the first run, this can take a while because Docker may need to pull the large `ollama/ollama` image first.

This lab uses `tinyllama` as the default local model because it is much smaller and more classroom-friendly than `llama3`.

The bridge container talks to Ollama through the Docker service name `ollama` on port `11434`. If you see a `500 Internal Server Error`, the first thing to check is whether both containers are healthy and whether `tinyllama` is already pulled.

## Step 3: Pull a Small Model

After the containers start, pull `tinyllama` into Ollama:

```bash
docker exec ollama ollama pull tinyllama
docker exec ollama ollama list
```

## Step 4: Point kubectl-ai at the Local Bridge

```bash
export KUBECTL_AI_PROVIDER="openai"
export OPENAI_API_BASE="http://localhost:8888/v1"
export OPENAI_API_KEY="local"
```

## Step 5: Test a Prompt

```bash
kubectl ai --llm-provider openai --model tinyllama "explain what a Kubernetes service does"
```

This path is now validated and works locally. Keep in mind that `tinyllama` is fast and lightweight, but the answer quality can be weak. It is fine for a quick demo of the integration. If you want better answers and your machine can handle it, pull a larger model and change `--model`.

If the response is empty, slow, or returns `500`, check whether Ollama has a model available and whether the containers are healthy.

## Verify the Environment

```bash
docker compose ps
docker compose logs --tail=50
docker exec ollama ollama list
```

You can also test the OpenAI-compatible endpoint directly:

```bash
curl -sS -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"tinyllama","messages":[{"role":"user","content":"explain what a Kubernetes service does"}]}'
```

## Cleanup

```bash
docker compose -f module8/local-mcp-ollama/docker-compose.yaml down -v
```

## What Just Happened?

You replaced a hosted LLM endpoint with a local one while keeping an OpenAI-compatible interface. This shows students that AI tooling is often just a thin layer around model APIs, and that those backends can be swapped when the interface stays stable.

In the next exercise, you will use this local endpoint with `kubectl-ai` so students can see AI-assisted Kubernetes prompts without depending on a hosted provider.
