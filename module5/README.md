# Module 5: Helm Chart Development

Module 5 converts the raw YAML deployment into a reusable Helm chart with environment-specific values.

## What Students Learn

1. Helm chart structure
2. values-driven configuration
3. local template rendering and linting
4. release installation, upgrade, history, and rollback
5. staging versus production overrides

## Architecture / Flow

This module converts the raw manifests from Module 2 into a reusable Helm chart:

- templates represent Kubernetes resources
- values files represent environment-specific configuration
- Helm release history supports upgrades and rollbacks

## Assets In This Module

- `chart/Chart.yaml`
- `chart/values.yaml`
- `chart/values-staging.yaml`
- `chart/values-production.yaml`
- `chart/templates/`
- `starter-chart/`
- `HELM_ARTIFACTHUB_AND_TEMPLATING_GUIDE.md`

## Prerequisites

- Modules 1 through 3 completed
- `helm` installed

## Step 1: Inspect the Chart Structure

```bash
cd module5
find chart -maxdepth 2 -type f | sort
```

Students should identify:

- chart metadata in `Chart.yaml`
- default configuration in `values.yaml`
- environment overrides in `values-staging.yaml` and `values-production.yaml`
- resource templates in `templates/`

## Step 2: Lint and Render the Chart

```bash
helm lint chart

helm template genai chart \
  --namespace genai-staging \
  -f chart/values-staging.yaml
```

Ask students to compare the rendered objects with the raw YAML they used in Module 2.

## Step 3: Clean Up the Module 2 Deployment If Reusing `genai`

If students already deployed the application into the `genai` namespace with raw YAML from Module 2, clean up those resources before installing the Helm release into the same namespace.

This avoids running two copies of the app side by side with different service names.

Example cleanup for the Module 2 app:

```bash
kubectl delete deployment api llm ui -n genai --ignore-not-found
kubectl delete service api-service llm-service ui-service -n genai --ignore-not-found
kubectl delete ingress genai-ingress -n genai --ignore-not-found
kubectl delete pvc ollama-models-pvc -n genai --ignore-not-found
```

Important note:

- only delete the Module 2 application resources you are replacing
- do not remove unrelated workloads in `genai` unless you intentionally want a full namespace reset

If students are installing Helm into a fresh namespace such as `genai-staging` or `genai-prod`, they do not need this cleanup step.

## Step 4: Install the Staging Release

```bash
helm upgrade --install genai chart \
  --namespace genai-staging \
  --create-namespace \
  -f chart/values-staging.yaml
```

Verify the release:

```bash
helm status genai -n genai-staging
kubectl get pods,svc,pvc -n genai-staging
```

## Step 5: Perform an Upgrade

Example upgrade:

```bash
helm upgrade genai chart \
  --namespace genai-staging \
  -f chart/values-staging.yaml \
  --set api.logLevel=WARNING
```

Review history:

```bash
helm history genai -n genai-staging
```

## Step 6: Roll Back the Release

```bash
helm rollback genai 1 -n genai-staging
helm history genai -n genai-staging
```

## Step 7: Deploy the Production Variant

```bash
helm upgrade --install genai chart \
  --namespace genai-prod \
  --create-namespace \
  -f chart/values-production.yaml
```

Validate:

```bash
kubectl get pods,svc,pvc -n genai-prod
```

## Troubleshooting

- If `helm lint` fails, inspect the template referenced in the error before attempting an install.
- If a release is stuck pending, use `helm status` and `kubectl get events -n <namespace>`.
- If the UI `NodePort` conflicts, override it with `--set ui.service.nodePort=<new-port>`.
- If students previously used Module 2 in the same namespace, confirm the old `api`, `llm`, `ui`, `api-service`, `llm-service`, and `ui-service` resources were deleted before the Helm install.

## Cleanup

```bash
helm uninstall genai -n genai-staging || true
helm uninstall genai -n genai-prod || true
kubectl delete namespace genai-staging --ignore-not-found
kubectl delete namespace genai-prod --ignore-not-found
```

## Instructor Validation Checklist

- `helm lint chart` succeeds
- `helm template` renders cleanly
- students can show one upgrade and one rollback in release history

## Suggested Teaching Thread

Use this module to show the progression:

- Module 2 taught raw manifests
- Module 3 added observability on top
- Module 5 turns the same platform into a reusable package for multiple environments

For extra practice with public charts and chart creation, use:

- [HELM_ARTIFACTHUB_AND_TEMPLATING_GUIDE.md](/home/arjun/advanced-k8s-genai/module5/HELM_ARTIFACTHUB_AND_TEMPLATING_GUIDE.md:1)
- [starter-chart](/home/arjun/advanced-k8s-genai/module5/starter-chart/Chart.yaml:1)

## Exit Criteria

Students are ready for Module 6 when:

- they can explain what `values.yaml` controls
- they can render and install the chart
- they can demonstrate one Helm upgrade and one rollback
