# 02: KEDA Installation

## Objective

Install KEDA so the cluster can scale workloads from external and Prometheus-based signals.

## Why This Matters

The Kubernetes HPA usually scales from CPU or memory. KEDA adds richer event-driven triggers, including direct queries against Prometheus.

## Step-by-step Instructions

### 1. Add the KEDA Helm repository

```bash
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
```

### 2. Install KEDA

```bash
helm upgrade --install keda kedacore/keda \
  --namespace keda \
  --create-namespace
```

### 3. Wait for KEDA to be ready

```bash
kubectl wait --for=condition=Available deployment/keda-operator -n keda --timeout=180s
kubectl get pods -n keda
```

### 4. Confirm the ScaledObject CRD exists

```bash
kubectl get crd scaledobjects.keda.sh
kubectl api-resources | grep ScaledObject
```

## Expected Outcome

- The `keda` namespace exists
- KEDA operator pods are running
- The `ScaledObject` resource is available in the cluster

## Validation

```bash
kubectl get deployment -n keda
kubectl get crd | grep keda.sh
```

## Troubleshooting

- If KEDA pods are pending, check node capacity with `kubectl get nodes`
- If the CRDs are missing, inspect the Helm release with `helm status keda -n keda`

## What Just Happened?

You installed the autoscaling controller that will translate a Prometheus latency query into actual replica changes on the API Deployment.
