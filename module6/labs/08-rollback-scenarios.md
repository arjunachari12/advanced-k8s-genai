# 08: Rollback Scenarios and Failure Handling

## Objective

Trigger a failed canary revision and observe how Argo Rollouts protects the stable version.

## Prerequisites

- Analysis template applied
- Load generator running

## Step-by-step Instructions

### 1. Trigger a bad revision

```bash
kubectl patch rollout genai-api -n genai-rollouts \
  --type json \
  -p='[{"op":"replace","path":"/spec/template/spec/containers/0/env/2/value","value":"http://invalid-llm.genai-rollouts.svc.cluster.local:11434"}]'
```

This revision points the API at a non-existent LLM endpoint, so requests should fail during the canary stage.

### 2. Watch the rollout fail

```bash
kubectl argo rollouts get rollout genai-api -n genai-rollouts -w
kubectl describe analysisrun -n genai-rollouts
```

### 3. Abort and undo if needed

```bash
kubectl argo rollouts abort genai-api -n genai-rollouts
kubectl argo rollouts undo genai-api -n genai-rollouts
```

Depending on timing, the rollout may already be aborted automatically by the failed analysis. In that case, `undo` is the main recovery action you need.

### 4. Restore the good configuration

```bash
kubectl apply -f module6/manifests/rollout.yaml
```

## Expected Output

- Analysis fails for the bad revision
- Rollout pauses or degrades
- Undo returns traffic to the previous good revision

## What Just Happened?

You tested the failure path of progressive delivery. The rollout controller allowed a limited canary attempt, analysis detected that the new revision was unhealthy, and the stable revision remained available for users.
