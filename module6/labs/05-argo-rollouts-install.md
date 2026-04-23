# 05: Argo Rollouts Installation

## Objective

Install Argo Rollouts and its CLI plugin so the cluster can run canary-style progressive delivery workflows.

## Prerequisites

- ArgoCD already installed

## Step-by-step Instructions

### 1. Install the controller

```bash
kubectl create namespace argo-rollouts --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl wait --for=condition=Ready pod --all -n argo-rollouts --timeout=300s
```

This adds the Rollout, AnalysisRun, and AnalysisTemplate CRDs plus the controller that watches them.

### 2. Install the CLI plugin

```bash
mkdir -p $HOME/.local/bin
curl -sSL -o $HOME/.local/bin/kubectl-argo-rollouts https://github.com/argoproj/argo-rollouts/releases/latest/download/kubectl-argo-rollouts-linux-amd64
chmod +x $HOME/.local/bin/kubectl-argo-rollouts
```

### 3. Verify the install

```bash
kubectl argo rollouts version
kubectl get pods -n argo-rollouts
```

## Expected Output

- Controller running in `argo-rollouts`
- `kubectl argo rollouts version` succeeds

## Troubleshooting

- If the plugin command is not found, make sure `$HOME/.local/bin` is on your `PATH`.
- If the controller pods are stuck, inspect them with `kubectl describe pod -n argo-rollouts`.
