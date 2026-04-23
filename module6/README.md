# Module 6: GitOps and Progressive Delivery with ArgoCD

Module 6 takes the Helm-based deployment from Module 5 and adds Git-driven reconciliation plus canary rollout workflows.

## What Students Learn

1. how to install ArgoCD
2. how to create an Argo Application from this repository
3. how auto-sync and self-heal work
4. how to detect and discuss configuration drift
5. how Argo Rollouts and Prometheus analysis support progressive delivery

## Architecture / Flow

- ArgoCD reads this repo and syncs the Helm chart from `module5/chart`
- Argo Rollouts manages a separate canary-focused API deployment
- Prometheus metrics decide whether canary steps continue or abort

## Assets In This Module

- `labs/01-argocd-installation.md` through `labs/08-rollback-scenarios.md`
- `manifests/argocd-app.yaml`
- `manifests/rollout.yaml`
- `manifests/analysis-template.yaml`
- supporting rollout manifests

## Prerequisites

- Module 5 completed
- repository pushed to a Git remote that ArgoCD can access
- `kubectl` and `helm` installed

The default `manifests/argocd-app.yaml` in this repo already points at the
current GitHub repository and the `main` branch. If you are teaching from a
fork, update `repoURL` and `targetRevision` before you apply it.

## Recommended Lab Order

1. `labs/01-argocd-installation.md`
2. `labs/02-create-application.md`
3. `labs/03-auto-sync-self-heal.md`
4. `labs/04-drift-detection.md`
5. `labs/05-argo-rollouts-install.md`
6. `labs/06-canary-deployment.md`
7. `labs/07-prometheus-analysis.md`
8. `labs/08-rollback-scenarios.md`

## Suggested Validation Commands

```bash
kubectl get pods -n argocd
argocd version --client
kubectl get applications -n argocd
kubectl get rollout -A
```

## Troubleshooting

- If ArgoCD login fails, keep the server port-forward open and use `--grpc-web`.
- If the application cannot sync, verify the Git repo URL and chart path in `manifests/argocd-app.yaml`.
- The rollout labs expect the `genai-gitops` Application to be healthy first because the canary API reuses the LLM service from that namespace.
- If rollouts do not progress, check `kubectl get analysisrun -n genai-rollouts` and confirm Prometheus is reachable.
- The first healthy canary request can still be slow while the LLM runtime warms up, so the latency analysis is tuned to tolerate warmup instead of enforcing a low web-style threshold.
- This repo uses the plain Prometheus Deployment from Module 3, so the rollout labs do not require `PodMonitor` or other Prometheus Operator CRDs.

## Cleanup

```bash
kubectl delete -f manifests/argocd-app.yaml --ignore-not-found
kubectl delete namespace genai-gitops --ignore-not-found
kubectl delete namespace genai-rollouts --ignore-not-found
kubectl delete namespace argo-rollouts --ignore-not-found
kubectl delete namespace argocd --ignore-not-found
```

## Instructor Validation Checklist

- ArgoCD is reachable from the browser and CLI
- `genai-gitops` syncs successfully from Git
- a canary rollout can progress and be rolled back

## Teaching Emphasis

This module is strongest when students compare three operating models:

- direct `kubectl apply`
- Helm release management
- GitOps reconciliation through ArgoCD

Then connect that to progressive delivery:

- canary steps
- metrics analysis
- rollback triggers

## Exit Criteria

Students are ready for Module 7 when:

- ArgoCD can sync an app from Git
- they understand why drift is corrected automatically
- they can explain how a canary rollout is gated by Prometheus data
