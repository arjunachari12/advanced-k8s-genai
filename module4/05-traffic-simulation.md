# 05: Traffic Simulation and Autoscaler Observation

## Objective

Generate enough API traffic to increase average latency and observe KEDA scale the backend.

## Files Used In This Exercise

- `manifests/load-generator-job.yaml`

## Step-by-step Instructions

### 1. Watch the Deployment and HPA

Open two terminals:

```bash
kubectl get deployment genai-genai-platform-api -n genai-staging -w
```

```bash
kubectl get hpa -n genai-staging -w
```

### 2. Start the load generator

```bash
kubectl apply -f module4/manifests/load-generator-job.yaml
```

Check the Job:

```bash
kubectl get jobs,pods -n genai-staging
kubectl logs -n genai-staging job/genai-api-load-generator
```

### 3. Watch the latency metric

If Prometheus is port-forwarded, query:

```text
genai_api_latency_avg_seconds{namespace="genai-staging"}
```

You should see the metric rise as the Job sends repeated `POST /generate` requests.

Important note:

- scale-up is not immediate
- expect roughly 1 to 2 minutes before the HPA and Deployment react
- that delay comes from Prometheus scrape timing, the `rate(...[2m])` query window, and KEDA polling

### 4. Observe scale-up

During sustained latency, check:

```bash
kubectl get deployment genai-genai-platform-api -n genai-staging
kubectl get pods -n genai-staging -l app.kubernetes.io/component=api
kubectl get events -n genai-staging --sort-by=.lastTimestamp | tail -n 20
```

### 5. Observe scale-down

After the Job finishes and the cooldown period expires:

```bash
kubectl get deployment genai-genai-platform-api -n genai-staging
kubectl get hpa -n genai-staging
```

### 6. Clean up the test traffic

```bash
kubectl delete job genai-api-load-generator -n genai-staging
```

## Expected Outcome

- The load generator produces repeated API calls
- average latency rises above the threshold
- KEDA increases the API replica count
- Replicas return toward the minimum count after traffic stops

## Troubleshooting

- If the Job finishes too quickly, delete it and re-apply after increasing `parallelism` or the loop count
- If latency does not cross the threshold, re-apply the Job after increasing `parallelism`, `completions`, or the request loop count
- If scaling does not happen, inspect the `ScaledObject` conditions with `kubectl describe scaledobject genai-api-latency -n genai-staging`

## Challenge Exercise

Change the threshold in the ScaledObject from `0.9` to `1.2` seconds and observe how the scaling behavior changes.
