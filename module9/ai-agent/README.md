# AI Kubernetes Assistant

This folder contains the implementation for the main Module 9 lab.

It packages a small LangGraph-based assistant that:

- runs inside Kubernetes
- calls read-only Kubernetes tools through the MCP server from Module 8
- uses an in-cluster Ollama model for summarization
- runs as either a one-shot Job or a scheduled CronJob

## What This Code Does

This is not a chatbot UI and it is not a general-purpose agent framework demo.

It is a focused operational worker.

Its purpose is to inspect a namespace, identify unhealthy workloads, collect the most relevant cluster signals, and print a beginner-friendly diagnosis with the next action to take.

## Why This Pattern Is Useful

For cloud and DevOps engineers, this shows a practical pattern:

- package the agent as a normal container
- run it with Kubernetes-native primitives
- keep tool access bounded through MCP
- keep model inference separate through Ollama
- inspect the result through normal Job logs

This makes the agent feel like platform automation, not a black-box AI app.

## Main Components

- `agent.py`: the LangGraph workflow that decides which tools to call and how to summarize the result
- `k8s/ollama.yaml`: the in-cluster Ollama deployment and service
- `k8s/job.yaml`: one-shot execution of the assistant
- `k8s/cronjob.yaml`: scheduled execution of the same assistant

## How The Agent Flow Works

At a high level:

1. fetch pod information from MCP
2. identify the most relevant unhealthy pod
3. fetch recent events
4. fetch logs only if the failure looks like a runtime issue
5. ask Ollama to produce a short diagnosis and exact next step

That means the workflow is agentic in a small, understandable way:

- it gathers information
- it decides what to inspect next
- it summarizes the result

## What Students Should Notice in `agent.py`

- `MCP_SERVER_URL` points to the in-cluster MCP service
- `OLLAMA_BASE_URL` points to the in-cluster model endpoint
- `TARGET_NAMESPACE` scopes the diagnosis target
- the LangGraph state tracks pod report, events, logs, and final answer
- common Kubernetes failure reasons such as image pull errors are converted into deterministic remediation guidance

## Build and Load

```bash
docker build -t ai-k8s-assistant:0.1.0 .
kind load docker-image ai-k8s-assistant:0.1.0 --name multi-node-cluster
```

## Run In Cluster

```bash
kubectl apply -f module9/ai-agent/k8s/ollama.yaml
kubectl rollout status deployment/ollama -n genai --timeout=600s
kubectl apply -f module9/ai-agent/k8s/job.yaml
```

Then read the result:

```bash
kubectl logs -n genai job/ai-k8s-assistant
```

## Why The Output Matters

The output is intentionally plain and operational:

- what failed
- why it likely failed
- what exact `kubectl` command to run next

That makes it useful for students who are learning troubleshooting, not just learning AI concepts.
