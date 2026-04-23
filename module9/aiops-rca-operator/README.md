# AIOps RCA Operator

This directory contains an optional advanced extension for Module 9.

## What This Is

This example combines:

- a Kubernetes Custom Resource Definition
- an operator handler
- a LangGraph workflow

The main custom resource is `RCARequest`.

When a user creates an `RCARequest`, the operator runs a multi-step investigation flow and writes the result back into the resource status.

## Why This Matters

This is the operator version of agentic troubleshooting.

Instead of manually launching a Job, a platform team could expose a Kubernetes-native API for root cause analysis requests.

That gives you:

- a declarative interface
- repeatable workflow execution
- status-based results
- a path toward richer platform automation

## How The Flow Works

At a high level:

1. `crd.yaml` defines `RCARequest`
2. `operator.py` watches for new requests
3. `graph.py` runs planner, debugger, analyzer, and fixer steps
4. the operator returns `analysis` and `fix` in the status output

## Files To Review

- `crd.yaml`
- `sample.yaml`
- `operator.py`
- `graph.py`
- `state.py`
- `agents/`

## Validation Level

This path was syntax-checked and also validated locally as an instructor extension during Module 9 work.

Use this folder as:

- an instructor extension
- an advanced design discussion
- a stretch lab for students who want a CRD-driven pattern

## Basic Walkthrough

Install dependencies:

```bash
python3 -m pip install --user -r requirements.txt
```

Apply the CRD:

```bash
kubectl apply -f crd.yaml
```

Run the operator locally:

```bash
kopf run operator.py --verbose
```

In another terminal, create a request:

```bash
kubectl get pods -n genai
# update sample.yaml with a real pod name first
kubectl apply -f sample.yaml
kubectl get rcarequest sample-rca -n genai -o yaml
```

If you want the planner/fixer steps to use Ollama while the operator runs on your laptop, port-forward the in-cluster Ollama service and point the operator to it:

```bash
kubectl port-forward -n genai svc/ollama 11434:11434
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

Without that port-forward, the operator still produces deterministic fixes for common Kubernetes failures such as image pull errors.

## Key Teaching Point

This example helps students connect three ideas from the course:

- Kubernetes APIs and operators
- MCP/tool-backed AI workflows
- agentic reasoning as a platform capability
