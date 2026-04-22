# Module 3: Observability with Prometheus, Loki, and Grafana

Module 3 adds metrics and logs to the application deployed in Module 2, still using plain manifests so students can see the raw Kubernetes building blocks.

## Learning Objectives

1. how Prometheus scrapes FastAPI metrics
2. how Grafana visualizes latency, errors, and request count
3. how Loki and Promtail collect pod logs
4. how to validate application health through observability instead of only `kubectl get pods`

## Architecture / Flow

- Prometheus scrapes the FastAPI `/metrics` endpoint.
- Grafana reads Prometheus and Loki as data sources.
- Loki stores logs.
- Promtail runs on nodes and ships pod logs to Loki.
- Alertmanager is not deployed in this module yet.

## Assets In This Module

- `monitoring/namespace.yaml`
- `monitoring/prometheus.yaml`
- `monitoring/grafana.yaml`
- `monitoring/loki.yaml`

## Prerequisites

- Module 2 completed
- the `genai` namespace workload is running

## Step 1: Confirm the API Exposes Metrics

The FastAPI app already exposes `/metrics` through the Prometheus instrumentator in `module2/api/app/main.py`.

Quick validation:

```bash
kubectl exec -n genai deploy/api -- python -c "import urllib.request; print('\n'.join(urllib.request.urlopen('http://127.0.0.1:8000/metrics').read().decode().splitlines()[:10]))"
```

## Step 2: Deploy the Monitoring Stack

```bash
cd module3

kubectl apply -f monitoring/namespace.yaml
kubectl apply -f monitoring/prometheus.yaml
kubectl apply -f monitoring/loki.yaml
kubectl apply -f monitoring/grafana.yaml
```

## Step 3: Verify the Monitoring Components

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

Expected components:

- Prometheus
- Grafana
- Loki
- Promtail

This module does not deploy:

- Alertmanager
- Prometheus Operator
- Kubernetes alert rules

## Step 4: Port-Forward the App and Monitoring UIs

Port-forward the Module 2 frontend so you can generate traffic:

```bash
kubectl -n genai port-forward svc/ui-service 8080:80
```

Open `http://127.0.0.1:8080`.

In a separate terminal, port-forward Grafana:

```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

Open `http://127.0.0.1:3000`.

Default credentials:

- username: `admin`
- password: `admin123`

In another terminal, port-forward Prometheus so you can inspect scrape targets and raw metrics:

```bash
kubectl -n monitoring port-forward svc/prometheus 9090:9090
```

Open `http://127.0.0.1:9090`.

Useful pages:

- Prometheus targets: `http://127.0.0.1:9090/targets`
- Prometheus graph: `http://127.0.0.1:9090/graph`
- Prometheus UI guide: `PROMETHEUS_UI_GUIDE.md`
- Grafana UI guide: `GRAFANA_UI_GUIDE.md`

For deeper walkthroughs:

- [Prometheus UI Guide](/home/arjun/advanced-k8s-genai/module3/PROMETHEUS_UI_GUIDE.md:1)
- [Grafana UI Guide](/home/arjun/advanced-k8s-genai/module3/GRAFANA_UI_GUIDE.md:1)

## Step 5: Generate Traffic and Read the Dashboards

Create a few requests against the app:

```bash
for i in 1 2 3 4 5; do
  curl -s -X POST http://127.0.0.1:8080/api/generate \
    -H "Content-Type: application/json" \
    -d '{"product":"AI notebook","audience":"platform teams"}' >/dev/null
done
```

Students should inspect:

- request count
- p95 latency
- error rate
- Prometheus target health for `api-service.genai.svc.cluster.local:8000`
- API logs flowing into Loki

## Validation Checks

```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
kubectl exec -n genai deploy/api -- python -c "import urllib.request; print('\n'.join(urllib.request.urlopen('http://127.0.0.1:8000/metrics').read().decode().splitlines()[:10]))"
```

Optional browser validations with the port-forwards above:

```bash
curl http://127.0.0.1:8080/healthz
curl http://127.0.0.1:3000/api/health
curl http://127.0.0.1:9090/api/v1/targets
```

## Troubleshooting

- If Grafana does not start, inspect `kubectl logs -n monitoring deploy/grafana`.
- If Prometheus charts are empty, confirm the `api` deployment is still running in `genai` and check `http://127.0.0.1:9090/targets`.
- If Loki logs are missing, inspect `kubectl logs -n monitoring ds/promtail`.
- If `curl http://127.0.0.1:8080/api/generate` is slow on the first request, give Ollama time to load the model.
- If you are looking for Alertmanager, note that it is not part of Module 3 yet.

## Cleanup

```bash
kubectl delete namespace monitoring --ignore-not-found
```

## Instructor Validation Checklist

- Prometheus, Grafana, Loki, and Promtail are all present in `monitoring`
- Prometheus shows the `genai` API target as `UP`
- Grafana dashboards show recent traffic
- Loki contains log lines from the `genai` namespace

## Discussion Prompt

Ask students:

1. what changed in the system after load was generated
2. where they can see the latency signal
3. which observability source is best for metrics versus raw log messages

## Exit Criteria

Students are ready for Module 4 when:

- Prometheus can scrape the API
- Grafana shows live data
- Loki contains logs from the application namespace
- students can reach the Module 2 app, Grafana, and Prometheus through port-forward
