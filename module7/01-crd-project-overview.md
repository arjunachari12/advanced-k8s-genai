# 01: The AI Workload Operator Project

## Overview

In this module, you will work with a custom Kubernetes Controller designed to manage the GenAI application you built in previous labs.

Instead of manually defining `Deployment` and `Service` manifests, this operator allows you to define a high-level `AIApp` resource. The operator then handles the "heavy lifting" of creating the underlying Kubernetes objects.

## The Custom Resource: `AIApp`

The project defines a Custom Resource Definition (CRD) named `AIApp`. This represents our application in the Kubernetes API.

### Key Fields (`Spec`)

The `AIApp` spec abstracts the complexity of the workload into a few simple fields:

- **`image`**: The container image to run (e.g., `arjunachari12/genai-api:1.0.0`).
- **`replicas`**: How many pods to run.
- **`modelName`**: The name of the model to request from Ollama (e.g., `tinyllama`).
- **`llmUrl`**: The internal URL of the LLM service.
- **`serviceType`**: How to expose the application (ClusterIP, NodePort, etc.).

### Status Reporting

The operator updates the `AIApp` status to reflect the real-world state of the application:

- **`phase`**: Are we `Pending` or `Ready`?
- **`readyReplicas`**: How many pods are actually up?
- **`deploymentName`**: The name of the generated child Deployment.

## The Controller Logic

The core logic lives in `internal/controller/aiapp_controller.go`. It runs a **Reconciliation Loop** that ensures the cluster state matches your `AIApp` definition.

### What the Controller Does

1. **Watches** for `AIApp` events (Create, Update, Delete).
2. **Generates** a `Deployment`:
   - It maps `spec.modelName` and `spec.llmUrl` to environment variables (`MODEL_NAME`, `LLM_URL`).
   - It configures Liveness and Readiness probes automatically.
   - It sets labels so the Deployment is "owned" by the `AIApp`.
3. **Generates** a `Service`:
   - It exposes the correct port defined in the spec.
4. **Heals** the application:
   - If you manually delete the generated Deployment, the controller sees the drift and recreates it immediately.
5. **Updates Status**:
   - It checks if the Deployment is ready and updates the `AIApp` status so you know when traffic can flow.

## Why Use This Pattern?

This pattern encodes "Operational Knowledge" into code. Instead of writing a wiki page that says *"Always set the MODEL_NAME env var and configure a readiness probe on port 8000,"* you write code that enforces those rules automatically.