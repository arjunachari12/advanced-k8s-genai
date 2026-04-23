# 02: Create the ArgoCD Application

## Objective

Create an ArgoCD `Application` that deploys the GenAI Helm chart into a dedicated GitOps namespace named `genai-gitops`.

## Prerequisites

- ArgoCD installed and running
- Repository pushed to a Git remote ArgoCD can access
- ArgoCD port-forward still running on `localhost:8081`

## Step-by-step Instructions

### 1. Log in to ArgoCD

```bash
argocd login localhost:8081 \
  --username admin \
  --password "$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d)" \
  --grpc-web \
  --insecure
```

### 2. Review the application manifest

Open:

`module6/manifests/argocd-app.yaml`

Before you apply it, update `repoURL` so it points at the Git repository and
branch that contain your current training repo structure. ArgoCD must be able
to find `module5/chart` in that remote repository.

If you are using this workshop repository directly, the default manifest already
points at the correct GitHub repo and `main` branch. You only need to edit it
when you are running from a fork or a different remote.

This application deploys the Helm chart to `genai-gitops`, uses `values-staging.yaml`, and overrides the UI service to `ClusterIP` so it does not conflict with the staging NodePort.

That separation is useful for training because it gives you one namespace managed directly by Helm from earlier labs and a second namespace managed entirely by ArgoCD.

### 3. Create the Application

```bash
kubectl apply -f module6/manifests/argocd-app.yaml
kubectl get applications -n argocd
```

### 4. Sync the Application

```bash
argocd app sync genai-gitops --grpc-web
argocd app wait genai-gitops --health --sync --grpc-web
```

## Expected Output

- A new ArgoCD application named `genai-gitops`
- Namespace `genai-gitops` created by ArgoCD
- Helm chart resources deployed and healthy

## Validation Steps

1. Check ArgoCD applications:
   ```bash
   kubectl get applications -n argocd
   ```
2. Check workload pods:
   ```bash
   kubectl get pods -n genai-gitops
   ```
3. Check app status:
   ```bash
   argocd app get genai-gitops --grpc-web
   ```

## Troubleshooting

- If sync fails, validate the chart with `helm template genai module5/chart --namespace genai-gitops -f module5/chart/values-staging.yaml`.
- If ArgoCD reports `app path does not exist`, the remote Git repo does not yet contain the current `module5/chart` path. Push your latest repo changes and update `repoURL` before syncing.
- If login fails, keep the port-forward open and use `--grpc-web`.
- If ArgoCD cannot read the repo, confirm the GitHub repo URL is public or add credentials in ArgoCD.

## What Just Happened?

You connected a Git repository, a Helm chart, and a Kubernetes namespace through one ArgoCD `Application`. From this point forward, ArgoCD can compare desired state in Git with live state in the cluster and report any differences.
