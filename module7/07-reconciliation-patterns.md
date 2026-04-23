# Exercise 7: Observe the Reconciliation Loop

This exercise shows what makes operators different from static manifests: they keep watching and correcting state.

## Scale the AIApp Through the Custom Resource

```bash
kubectl patch aiapp aiapp-sample \
  -n ai-operators-lab \
  --type merge \
  -p '{"spec":{"replicas":2}}'
```

Watch the deployment:

```bash
kubectl get deployment aiapp-sample -n ai-operators-lab -w
```

In another terminal, inspect the custom resource status:

```bash
kubectl get aiapp aiapp-sample -n ai-operators-lab -o yaml
```

You should see:

- `spec.replicas: 2`
- `status.readyReplicas: 2`
- `status.phase: Ready`

## Change the Log Level

```bash
kubectl patch aiapp aiapp-sample \
  -n ai-operators-lab \
  --type merge \
  -p '{"spec":{"logLevel":"DEBUG"}}'
```

Confirm the Deployment template changed:

```bash
kubectl get deployment aiapp-sample -n ai-operators-lab -o yaml | grep -A3 LOG_LEVEL
```

## Map the Design Pattern

This operator follows a classic reconciliation model:

1. read current desired state from the custom resource
2. compare it to real cluster state
3. create or update owned resources
4. write back status so users can understand progress
5. repeat whenever spec or owned resources change

## What Just Happened?

The controller kept running after the first object creation. When you edited the `AIApp`, the operator noticed the change, reconciled the managed `Deployment`, and updated status again. That continuous loop is the heart of controller design.
