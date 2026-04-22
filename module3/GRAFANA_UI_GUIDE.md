# Grafana UI Guide

This guide teaches students how to navigate the Grafana UI used in Module 3.

## Prerequisites

- Module 2 is running in the `genai` namespace
- Module 3 monitoring manifests are applied
- Grafana is port-forwarded:

```bash
kubectl -n monitoring port-forward svc/grafana 3000:3000
```

Open `http://127.0.0.1:3000`.

Default credentials:

- username: `admin`
- password: `admin123`

## First Navigation Steps

What students should notice:

- the left sidebar is used for dashboards, explore, and administration
- `Dashboards` is the quickest way to start with a guided view
- `Explore` is for ad hoc metrics and log investigation
- the time picker controls the visible time range
- the refresh control helps students watch new data arrive

Recommended first clicks:

1. Sign in to Grafana.
2. Open `Dashboards`.
3. Open the `Workshop` folder.
4. Open `GenAI Observability Overview`.
5. Set the time range to the last `15 minutes`.
6. Refresh after generating traffic from the app.

## What This Dashboard Shows

The provisioned dashboard includes:

- `Request Count` from Prometheus
- `Latency (p95)` from Prometheus
- `Error Rate` from Prometheus
- `API Logs` from Loki

How to explain the dashboard:

- use `Request Count` to confirm traffic is reaching the app
- use `Latency (p95)` to see whether responses are slowing down
- use `Error Rate` to see whether failures are increasing
- use `API Logs` to inspect the application messages behind the metrics

## Learn Grafana Explore

Open `Explore` from the left sidebar.

Students can switch between:

- `Prometheus` for metrics queries
- `Loki` for log queries

Good Prometheus queries to try:

```promql
sum(rate(http_requests_total{handler!="/metrics"}[1m]))
```

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{handler!="/metrics"}[5m])) by (le))
```

```promql
sum(rate(http_requests_total{status=~"5..",handler!="/metrics"}[5m])) / sum(rate(http_requests_total{handler!="/metrics"}[5m]))
```

Good Loki query to try:

```logql
{namespace="genai", app="api"}
```

What students learn in Explore:

- dashboards are curated views for fast reading
- Explore is where they ask one-off questions
- Prometheus explains counts, rates, and latency
- Loki explains what the application actually logged
- using both together helps correlate symptoms with evidence

## Good Classroom Flow

1. Generate traffic from `http://127.0.0.1:8080`.
2. Refresh the `GenAI Observability Overview` dashboard.
3. Watch `Request Count` increase.
4. Observe `Latency (p95)`, especially during the first Ollama-backed request.
5. Open `Explore` and run `{namespace="genai", app="api"}`.
6. Match the log timestamps with the dashboard changes.

## Quick Validation

```bash
curl http://127.0.0.1:3000/api/health
```

The Grafana health API should respond with JSON showing the database status is `ok`.
