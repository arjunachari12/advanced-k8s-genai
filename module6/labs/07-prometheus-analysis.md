# 07: Prometheus Analysis for Rollout Validation

## Objective

Use Prometheus metrics to decide whether a canary step should continue.

## Prerequisites

- Rollout running in `genai-rollouts`
- Load generator running
- `genai-gitops` Application healthy

## Step-by-step Instructions

### 1. Verify the AnalysisTemplate

```bash
kubectl get analysistemplates -n genai-rollouts
```

The template checks two signals:

- request success rate
- average request latency

These queries run against the plain Prometheus service from Module 3:

`http://prometheus.monitoring.svc.cluster.local:9090`

The latency threshold in this workshop is intentionally generous because the
first LLM-backed response in a fresh canary can take tens of seconds while the
model runtime warms up. That keeps the lab focused on rollout mechanics while
still demonstrating a Prometheus-backed quality gate.

### 2. Trigger another revision

```bash
kubectl patch rollout genai-api -n genai-rollouts \
  --type json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/env/1/value","value":"DEBUG"}]'
```

### 3. Monitor the rollout and analysis

```bash
kubectl argo rollouts get rollout genai-api -n genai-rollouts -w
kubectl get analysisruns -n genai-rollouts
```

## Expected Output

- Analysis runs created during canary steps
- Healthy metrics allow rollout progression
- During the very first scrape window, metrics may need 15 to 30 seconds to populate before the analysis turns green
- You will often see a short `Paused` state first because the rollout includes timed canary pause steps before each analysis gate

## Validation Steps

```bash
kubectl get analysistemplates -n genai-rollouts
kubectl describe analysisrun -n genai-rollouts
```

## What Just Happened?

You inserted an automated quality gate into the rollout itself. Instead of promoting a canary only because pods are up, the controller now waits for application-level metrics to pass.
