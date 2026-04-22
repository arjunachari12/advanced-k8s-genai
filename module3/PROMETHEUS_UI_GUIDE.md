# Prometheus UI Guide

This guide teaches students how to navigate the Prometheus UI used in Module 3.

## Prerequisites

- Module 2 is running in the `genai` namespace
- Module 3 monitoring manifests are applied
- Prometheus is port-forwarded:

```bash
kubectl -n monitoring port-forward svc/prometheus 9090:9090
```

Open `http://127.0.0.1:9090`.

## Start With Targets

Open `http://127.0.0.1:9090/targets`.

Students should verify:

- the `prometheus` self-scrape target is `UP`
- the `genai-api` target for `api-service.genai.svc.cluster.local:8000` is `UP`

If the `genai-api` target is down, Prometheus cannot scrape the FastAPI metrics endpoint.

## Learn the Graph Page

Open `http://127.0.0.1:9090/graph`.

What students should notice:

- the expression bar is where they type a metric name or PromQL query
- `Table` shows the latest value for each time series
- `Graph` shows how values change over time
- `Execute` runs the current query
- the time controls help zoom into recent traffic

Recommended first clicks:

1. Open the `Graph` page.
2. Type a simple metric name.
3. Run it in `Table` view first.
4. Switch to `Graph` view after generating traffic.
5. Change the time range to the last few minutes.

## Beginner-Friendly Queries

```promql
http_requests_total
```

Shows the raw request counter series exported by the FastAPI app.

```promql
http_requests_total{handler="/generate"}
```

Filters the series to the `/generate` endpoint only.

```promql
sum(rate(http_requests_total{handler!="/metrics"}[1m]))
```

Shows requests per second across the app, excluding Prometheus scrape traffic.

```promql
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{handler!="/metrics"}[5m])) by (le))
```

Shows p95 request latency.

```promql
sum(rate(http_requests_total{status=~"5..",handler!="/metrics"}[5m])) / sum(rate(http_requests_total{handler!="/metrics"}[5m]))
```

Shows the 5xx error ratio.

## How To Explain The Results

- `http_requests_total` is a counter, so it increases over time
- labels like `handler`, `method`, and `status` let students filter or split one metric
- `rate(metric[1m])` converts a counter into a per-second trend
- `sum(...)` combines matching time series into a single value
- `histogram_quantile(...)` estimates latency percentiles from histogram buckets

## Good Classroom Flow

1. Run `http_requests_total` before any traffic and note the baseline.
2. Send 5 to 10 requests to the app through `http://127.0.0.1:8080`.
3. Re-run `http_requests_total{handler="/generate"}` and confirm the counter increased.
4. Run `sum(rate(http_requests_total{handler!="/metrics"}[1m]))` and switch to `Graph`.
5. Compare the Prometheus signal with the Grafana dashboard panels.

## Quick Validation

```bash
curl http://127.0.0.1:9090/api/v1/targets
```

You can also confirm the application exports metrics directly:

```bash
kubectl exec -n genai deploy/api -- python -c "import urllib.request; print('\n'.join(urllib.request.urlopen('http://127.0.0.1:8000/metrics').read().decode().splitlines()[:10]))"
```
