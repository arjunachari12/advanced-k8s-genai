# Module 9: Agentic AI Systems on Kubernetes

Module 9 turns the read-only MCP pattern from Module 8 into a real in-cluster agent workflow.

Students are no longer just prompting an AI tool from their laptop. In this module, they run an agent inside Kubernetes that:

- inspects live cluster state through MCP
- reasons about what to investigate next
- summarizes the result with a local Ollama model
- runs as a Kubernetes Job or CronJob

## What Students Build

The main build artifact in this module is an AI operations assistant packaged as a Kubernetes workload.

This assistant is not a chatbot UI. It is an operational worker that runs in-cluster and diagnoses failures in the `genai` namespace.

The module also includes an optional advanced extension:

- a CRD-driven AIOps root cause analysis operator

## Why This Matters

This module helps students understand the next step after prompt engineering and MCP:

- how an agent can choose tools instead of relying on one prompt
- how Kubernetes can act as the runtime for AI workflows
- how safe read-only diagnostics can be automated on a schedule

For cloud and platform engineers, this is the practical takeaway:

you can package AI-assisted operational logic as a standard Kubernetes workload, with clear inputs, dependencies, permissions, and outputs.

## Architecture

- `mcp-server` from Module 8 provides read-only Kubernetes tools
- `ollama` provides in-cluster model inference
- the LangGraph assistant decides which cluster data to fetch
- a Job or CronJob provides execution and scheduling

## Module Flow

1. `01-run-the-ai-agent-job.md`
2. `02-schedule-the-agent-with-a-cronjob.md`
3. `03-optional-aiops-rca-operator.md`

## Assets In This Module

- `ai-agent/` - LangGraph assistant, Dockerfile, and Kubernetes manifests
- `aiops-rca-operator/` - optional CRD-driven RCA experiment

## Validated Commands

The following commands were validated on the shared KIND cluster on April 24, 2026:

```bash
python3 -m py_compile module9/ai-agent/agent.py module9/aiops-rca-operator/operator.py module9/aiops-rca-operator/graph.py module9/aiops-rca-operator/state.py module9/aiops-rca-operator/agents/*.py module9/aiops-rca-operator/tools/*.py
docker build -t ai-k8s-assistant:0.1.0 module9/ai-agent
kind load docker-image ai-k8s-assistant:0.1.0 --name multi-node-cluster
kubectl apply -f module9/ai-agent/k8s/ollama.yaml
kubectl rollout status deployment/ollama -n genai --timeout=600s
kubectl create deployment broken-redis --image=redis:this-tag-does-not-exist -n genai --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f module9/ai-agent/k8s/job.yaml
kubectl wait --for=condition=complete job/ai-k8s-assistant -n genai --timeout=300s
kubectl logs -n genai job/ai-k8s-assistant
```

## Prerequisites

- Module 8 completed
- the `mcp-server` from Module 8 deployed in `genai`
- Docker available locally
- a working KIND cluster named `multi-node-cluster`

## Quick Start

If you want the shortest path through the module:

1. Follow `01-run-the-ai-agent-job.md` to build the agent image and run a one-shot diagnosis Job.
2. Follow `02-schedule-the-agent-with-a-cronjob.md` to turn the same logic into a periodic cluster check.
3. Optionally explore `03-optional-aiops-rca-operator.md` to see how the same idea can be wrapped in a CRD and operator pattern.

## Instructor Goals

- students can explain how the agent gets live cluster context
- students can trace how the agent chooses which tools to use
- students can explain why the MCP layer stays read-only
- students can explain why Kubernetes Jobs and CronJobs are a good runtime for this pattern

## Exit Criteria

Students are ready for the next step when they can explain:

- where the agent gets its data
- where the model runs
- how Kubernetes schedules the work
- why tool access and RBAC boundaries still matter in agentic systems
