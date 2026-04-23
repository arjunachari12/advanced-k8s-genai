# 03: Auto-Sync, Self-Healing, and Pruning

## Objective

Enable automated reconciliation so ArgoCD can correct drift without a manual sync command.

## Prerequisites

- `genai-gitops` application created
- ArgoCD CLI logged in

## Step-by-step Instructions

### 1. Enable automated sync

```bash
argocd app set genai-gitops \
  --sync-policy automated \
  --self-heal \
  --auto-prune \
  --grpc-web
```

### 2. Confirm the setting

```bash
argocd app get genai-gitops --grpc-web
```

### 3. Test self-healing

Create drift by scaling the API deployment away from Git:

```bash
kubectl scale deployment genai-genai-platform-api -n genai-gitops --replicas=2
kubectl get deployment genai-genai-platform-api -n genai-gitops
```

Wait for ArgoCD to reconcile:

```bash
argocd app wait genai-gitops --sync --health --grpc-web --timeout 180
kubectl get deployment genai-genai-platform-api -n genai-gitops
```

## Expected Output

- Auto-sync enabled
- Manual drift reverted by ArgoCD
- Deployment returns to the Git-defined replica count

## Validation Steps

1. Check app config:
   ```bash
   argocd app get genai-gitops --grpc-web
   ```
2. Check history:
   ```bash
   argocd app history genai-gitops --grpc-web
   ```

## Troubleshooting

- If drift is not corrected, confirm the application is in automated mode.
- If the app stays out of sync, inspect the controller logs in `argocd`.
- If you see `repository not accessible` or `connection refused`, the repo server may be down. Check it with `kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-repo-server`.

## What Just Happened?

You enabled the core GitOps loop. ArgoCD now watches for differences between Git and the cluster, then applies the Git-defined state automatically.
