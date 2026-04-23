# 01: Prometheus Adapter Installation

## Objective

Install Prometheus Adapter so Kubernetes can expose Prometheus-backed custom metrics through the custom metrics API.

## Why This Matters

Prometheus stores the raw time series, but Kubernetes-native autoscaling tools often expect metrics to be available through the Kubernetes metrics APIs.

Prometheus Adapter bridges that gap.

## Prerequisites

- Module 5 observability stack is running
- Prometheus is available in the `monitoring` namespace

## Files Used In This Exercise

- `manifests/prometheus-adapter-values.yaml`

## Step-by-step Instructions

### 1. Add the Helm repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 2. Install Prometheus Adapter

```bash
helm upgrade --install prometheus-adapter prometheus-community/prometheus-adapter \
  --namespace monitoring \
  --create-namespace \
  -f module4/manifests/prometheus-adapter-values.yaml
```

### 3. Wait for the adapter to be ready

```bash
kubectl rollout status deployment/prometheus-adapter -n monitoring --timeout=180s
kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus-adapter
```

### 4. Check that the custom metrics API is registered

```bash
kubectl get apiservice | grep custom.metrics
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1 | python3 -m json.tool
```

## Expected Outcome

- The `prometheus-adapter` Deployment is running in `monitoring`
- The `custom.metrics.k8s.io` APIService is available

## Validation

```bash
kubectl get deployment prometheus-adapter -n monitoring
kubectl get apiservice v1beta1.custom.metrics.k8s.io
```

## Troubleshooting

- If the Deployment is not ready, inspect logs with `kubectl logs -n monitoring deployment/prometheus-adapter`
- If the APIService shows `False`, describe it with `kubectl describe apiservice v1beta1.custom.metrics.k8s.io`

## What Just Happened?

You installed a bridge between Prometheus and the Kubernetes custom metrics API. In the next exercise, we will give that adapter a latency metric to expose.
