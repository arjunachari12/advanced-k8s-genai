# 04: Latency-Based ScaledObject

## Objective

Create a KEDA `ScaledObject` that increases API replicas when the average request latency stays above the threshold.

## Files Used In This Exercise

- `manifests/keda-scaledobject.yaml`

## Step-by-step Instructions

### 1. Inspect the current API replica count

```bash
kubectl get deployment genai-genai-platform-api -n genai-staging
```

### 2. Apply the ScaledObject

```bash
kubectl apply -f module4/manifests/keda-scaledobject.yaml
```

### 3. Verify that KEDA created the HPA

```bash
kubectl get scaledobject -n genai-staging
kubectl get hpa -n genai-staging
kubectl describe scaledobject genai-api-latency -n genai-staging
```

### 4. Understand the threshold

This ScaledObject queries:

```text
sum(rate(http_request_duration_seconds_sum{namespace="genai-staging",handler="/generate",method="POST"}[2m])) by (namespace)
/
sum(rate(http_request_duration_seconds_count{namespace="genai-staging",handler="/generate",method="POST"}[2m])) by (namespace)
```

This keeps the trigger centered on latency while allowing the signal to fall back down as request traffic drains away.

It scales when the effective value rises above `0.9`.

## Expected Outcome

- A `ScaledObject` named `genai-api-latency` exists
- KEDA creates an HPA for the API Deployment
- The Deployment is now managed by KEDA for replica changes

## Validation

```bash
kubectl get scaledobject genai-api-latency -n genai-staging -o yaml
kubectl get hpa -n genai-staging
```

## Troubleshooting

- If the HPA does not appear, inspect operator logs with `kubectl logs -n keda deployment/keda-operator`
- If the query returns no data, go back to Exercise 3 and confirm Prometheus is scraping the staging API service

## What Just Happened?

You connected a Prometheus latency query to a Kubernetes Deployment through KEDA. The next exercise will create traffic so that query crosses the scaling threshold.
