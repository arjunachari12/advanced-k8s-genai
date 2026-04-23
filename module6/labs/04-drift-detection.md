# 04: Drift Detection and Reconciliation

## Objective

Observe how ArgoCD reports drift before or while it reconciles the cluster back to the Git-defined state.

## Prerequisites

- `genai-gitops` app synced and healthy
- Auto-sync enabled

## Step-by-step Instructions

### 1. Confirm the app is healthy

```bash
argocd app get genai-gitops --grpc-web
```

### 2. Introduce drift

```bash
kubectl scale deployment genai-gitops-genai-platform-api -n genai-gitops --replicas=3
```

### 3. Inspect the diff

```bash
argocd app diff genai-gitops --grpc-web
```

### 4. Watch reconciliation

```bash
argocd app wait genai-gitops --sync --health --grpc-web --timeout 180
kubectl get deployment genai-genai-platform-api -n genai-gitops
```

## Expected Output

- ArgoCD reports the Deployment drift
- The application returns to `Synced`
- Replica count returns to the Git state

## Validation Steps

```bash
argocd app get genai-gitops --grpc-web
kubectl get deployment genai-genai-platform-api -n genai-gitops -o jsonpath='{.spec.replicas}'
```

## What Just Happened?

You forced a live-state change in the cluster and let ArgoCD compare that live state to the manifest rendered from Git. That comparison is the foundation of drift detection.
