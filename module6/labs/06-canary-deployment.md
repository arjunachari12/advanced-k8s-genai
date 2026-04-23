# 06: Canary Deployment with Argo Rollouts

## Objective

Deploy a focused API rollout in `genai-rollouts` and trigger a canary revision without disturbing the GitOps-managed Helm release in `genai-gitops`.

## Prerequisites

- Argo Rollouts installed
- Prometheus stack running
- `genai-gitops` Application synced and healthy

## Step-by-step Instructions

### 1. Create the rollout namespace

```bash
kubectl create namespace genai-rollouts --dry-run=client -o yaml | kubectl apply -f -
```

### 2. Apply the service and AnalysisTemplate

```bash
kubectl apply -f module6/manifests/service.yaml
kubectl apply -f module6/manifests/analysis-template.yaml
```

### 3. Apply the rollout

```bash
kubectl apply -f module6/manifests/rollout.yaml
```

The rollout starts with a stable revision that points at the same API image used elsewhere in the workshop.
It reuses the LLM service from the GitOps-managed `genai-gitops` namespace so
the canary lab stays aligned with the ArgoCD flow from the earlier steps.

### 4. Start background traffic

```bash
kubectl apply -f module6/manifests/rollout-load-generator.yaml
```

This traffic source is important because the Prometheus analysis checks need live request data.

### 5. Trigger a canary update

```bash
kubectl patch rollout genai-api -n genai-rollouts \
  --type json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/env/1/value","value":"WARNING"}]'
```

This command changes only the `LOG_LEVEL` environment variable. That is enough to create a new ReplicaSet and start a canary rollout, while keeping the application behavior healthy.

### 6. Watch the rollout

```bash
kubectl argo rollouts get rollout genai-api -n genai-rollouts -w
```

The rollout will pause at the built-in canary pause steps before it runs
analysis. That is expected. Keep the watch open and let the controller advance
through the timed pauses.

## Expected Output

- Rollout progresses through `20%`, `50%`, then `100%`
- Old and new ReplicaSets appear during the canary
- Analysis runs are created at the canary checkpoints

## Validation Steps

```bash
kubectl argo rollouts get rollout genai-api -n genai-rollouts
kubectl get pods -n genai-rollouts
```

## What Just Happened?

You created a second deployment path just for progressive delivery experiments. Argo Rollouts now controls how quickly a new ReplicaSet is introduced and whether analysis should pause or stop that promotion.
