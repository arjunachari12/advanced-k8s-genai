# Module 8: AI-Augmented Kubernetes with Local Ollama, kubectl-ai, and MCP

This module works best as a three-step story:

1. start with a local Ollama-backed endpoint so students can demo AI without needing a hosted API key
2. use `kubectl-ai` as an AI assistant for Kubernetes work
3. build and run your own read-only Kubernetes MCP server so AI tooling can safely inspect cluster state

## What Students Build

Students do not build a Kubernetes application in this module. They build an AI-assisted operations workflow.

The module has three connected pieces:

- a local Ollama bridge that exposes an OpenAI-compatible API on the laptop
- `kubectl-ai`, which lets students ask for manifests, explanations, and troubleshooting help in natural language
- a custom read-only MCP server, which exposes a small set of safe Kubernetes tools such as listing nodes, namespaces, pods, logs, and events

By the end of the module, students should understand the difference between:

- asking an LLM for advice
- giving an AI assistant real, controlled tools to inspect a cluster

## Why This Matters

Plain prompting is useful, but it has limits. An AI model without tools can only guess based on the text you provide.

An MCP server changes that. It gives the AI assistant structured access to real cluster data through a bounded interface. In this module, that interface is intentionally read-only, which makes it a good teaching example for safe AI integration.

This helps students see:

- why AI answers improve when the assistant can inspect real state
- why permission boundaries matter
- how platform teams can expose safe capabilities instead of handing out full cluster-admin access

## Module Flow

1. `01-local-ollama-foundation.md`
2. `02-kubectl-ai-basics.md`
3. `03-build-and-run-mcp-server.md`

## Assets In This Module

- `mcp-server/` - Python MCP server, sample client, Dockerfile, and Kubernetes manifests
- `local-mcp-ollama/` - OpenAI-compatible bridge to Ollama for local/private demos

## Validated Commands

The following commands were validated on the shared KIND cluster on April 24, 2026:

```bash
python3 -m py_compile module8/mcp-server/server.py module8/mcp-server/client.py module8/local-mcp-ollama/server.py
python3 -m pip install --user -r module8/mcp-server/requirements.txt
docker build -t mcp-k8s-server:0.1.0 module8/mcp-server
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
kubectl apply -f module8/mcp-server/k8s/rbac.yaml
kubectl apply -f module8/mcp-server/k8s/deployment.yaml
kubectl rollout status deployment/mcp-server -n genai
kubectl port-forward -n genai svc/mcp-server-svc 8000:80
python3 module8/mcp-server/client.py
docker compose -f module8/local-mcp-ollama/docker-compose.yaml config
```

## Prerequisites

- a working KIND cluster
- `kubectl` configured
- Docker available locally
- Modules 1 through 3 complete

## Quick Start

If you want the shortest path through the module:

1. Follow `01-local-ollama-foundation.md` to stand up a local AI backend that works without a hosted provider key.
2. Follow `02-kubectl-ai-basics.md` to install and try `kubectl-ai` against either local Ollama, Gemini, or OpenAI.
3. Follow `03-build-and-run-mcp-server.md` to deploy the read-only MCP server and connect AI tooling to live cluster data.

## Instructor Goals

- students can explain what `kubectl-ai` does well and where it is limited
- students can explain what the MCP server adds
- students can point to the read-only RBAC and describe why it is safer than broad write access
- students can successfully query live cluster information through the MCP server

## Exit Criteria

Students are ready for the next module when they can:

- use AI once for manifest generation or explanation
- use AI once for troubleshooting with live cluster context
- explain why a read-only MCP server is safer than directly exposing full Kubernetes credentials to an LLM tool
