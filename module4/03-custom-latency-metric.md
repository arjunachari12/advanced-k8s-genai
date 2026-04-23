# 03: Custom Latency Metric

## Objective

Expose API latency through Prometheus Adapter as a Kubernetes custom metric.

## Files Used In This Exercise

- `module3/monitoring/prometheus.yaml`
- `manifests/prometheus-adapter-values.yaml`

## Step-by-step Instructions

### 1. Ensure Prometheus is scraping the staging API service

This repository uses the plain Prometheus Deployment from Module 3, so the
staging scrape target is defined in `module3/monitoring/prometheus.yaml`.

Re-apply the Prometheus manifest if needed:

```bash
kubectl apply -f module3/monitoring/prometheus.yaml
kubectl rollout restart deployment/prometheus -n monitoring
kubectl rollout status deployment/prometheus -n monitoring --timeout=180s
```

Verify the scrape configuration:

```bash
kubectl get configmap prometheus-config -n monitoring -o yaml
```

### 2. Generate a few requests so the metric appears

Port-forward the UI or call the API service directly:

```bash
kubectl -n genai-staging port-forward svc/genai-genai-platform-ui 8080:80
```

In another terminal:

```bash
for i in $(seq 1 5); do
  curl -s -X POST http://127.0.0.1:8080/api/generate \
    -H "Content-Type: application/json" \
    -d '{
      "product": "Latency demo",
      "audience": "platform engineers"
    }' > /dev/null
done
```

### 3. Query the latency signal in Prometheus

Port-forward Prometheus:

```bash
kubectl -n monitoring port-forward svc/prometheus 9090:9090
```

In the Prometheus UI, run:

```text
sum(rate(http_request_duration_seconds_sum{namespace="genai-staging",handler="/generate",method="POST"}[2m])) by (namespace)
/
sum(rate(http_request_duration_seconds_count{namespace="genai-staging",handler="/generate",method="POST"}[2m])) by (namespace)
```

### 4. Query the custom metric through Kubernetes

```bash
kubectl get --raw \
  "/apis/custom.metrics.k8s.io/v1beta1/namespaces/genai-staging/metrics/genai_api_latency_avg_seconds" | python3 -m json.tool
```

## Expected Outcome

- Prometheus scrapes the staging API service
- Prometheus Adapter exposes `genai_api_latency_avg_seconds` through `custom.metrics.k8s.io`

## Troubleshooting

- If the metric is empty, wait 1 to 2 scrape intervals and send more traffic
- If the custom metrics query fails, make sure Exercise 1 completed successfully
- If Prometheus still only scrapes the `genai` namespace app, re-apply `module3/monitoring/prometheus.yaml`

## What Just Happened?

You exposed a Prometheus latency query through the Kubernetes custom metrics API without needing Prometheus Operator CRDs.
