# Module 4: Autoscaling with KEDA and Prometheus Metrics

## Learning Objectives

1. Install Prometheus Adapter
2. Install KEDA
3. Create a reusable p95 latency metric from Prometheus
4. Expose that metric through the Kubernetes custom metrics API
5. Scale the FastAPI API deployment when latency rises
6. Generate traffic and observe the scale-up and scale-down flow

## Architecture / Flow

This module starts from the Helm-based staging environment created in Module 5:

- Prometheus already scrapes the API
- Prometheus Adapter exposes a custom metric to Kubernetes
- KEDA reads that metric and changes replica count
- a load generator creates traffic that drives scaling

## Prerequisites

- A running KIND cluster
- Module 5 completed in the `genai-staging` and `monitoring` namespaces
- `kubectl` configured for the cluster
- `helm` installed

Recommended validation before you begin:

```bash
kubectl get pods -n monitoring
kubectl get pods -n genai-staging
kubectl get configmap prometheus-config -n monitoring
```

## Module Structure

1. [01-prometheus-adapter-installation.md](01-prometheus-adapter-installation.md)
2. [02-keda-installation.md](02-keda-installation.md)
3. [03-custom-latency-metric.md](03-custom-latency-metric.md)
4. [04-latency-based-scaledobject.md](04-latency-based-scaledobject.md)
5. [05-traffic-simulation.md](05-traffic-simulation.md)

## Supporting Files

All manifests for this module live in:

`manifests/`

## Validation Checks

```bash
kubectl get apiservice | grep custom.metrics
kubectl get scaledobject -n genai-staging
kubectl get hpa -n genai-staging
kubectl get pods -n genai-staging -w
```

## Troubleshooting

- If custom metrics are missing, re-check the Prometheus Adapter values and APIService status.
- If the API never scales, verify the load generator is running and Prometheus has recent request data.
- If KEDA is installed but idle, inspect `kubectl logs -n keda deploy/keda-operator`.
- This repo uses the plain Prometheus Deployment from Module 3, not Prometheus Operator CRDs such as `PodMonitor` or `PrometheusRule`.

## Cleanup

```bash
kubectl delete -f manifests/load-generator-job.yaml --ignore-not-found
kubectl delete -f manifests/keda-scaledobject.yaml --ignore-not-found
```

## Instructor Validation Checklist

- custom metrics API is available
- `ScaledObject` exists in `genai-staging`
- replica count increases under load and decreases afterward
