# Exercise 6: Create Custom Resources

Now you will create `AIApp` objects and let the operator manage the real workload.

## Apply the Full Sample

The first sample sets every important field explicitly.

```bash
cd module7
kubectl apply -f config/samples/ai_v1alpha1_aiapp.yaml
```

Inspect the resource:

```bash
kubectl get aiapp -n ai-operators-lab
kubectl get aiapp -n ai-operators-lab aiapp-sample -o yaml
```

Inspect the managed workload:

```bash
kubectl get deployment,svc,pods -n ai-operators-lab -o wide
kubectl wait --for=condition=available deployment/aiapp-sample -n ai-operators-lab --timeout=180s
```

Expected result:

- an `AIApp` named `aiapp-sample`
- a matching `Deployment`
- a matching `Service`
- one running API pod
- `status.phase: Ready`

## Apply the Minimal Sample

The second sample demonstrates controller-side defaults.

```bash
kubectl apply -f config/samples/ai_v1alpha1_aiapp_minimal.yaml
kubectl get aiapp -n ai-operators-lab aiapp-defaults-demo -o yaml
kubectl get deployment,svc,pods -n ai-operators-lab
```

Notice that the CRD and controller still produce a working workload even though the custom resource did not specify every field. Some values are defaulted into the custom resource itself, while others are applied when the controller builds the managed Deployment and Service.

## What Just Happened?

You used the custom API exactly the way a platform user would. Instead of hand-writing a `Deployment` and `Service`, you created a higher-level `AIApp` resource and let the operator translate that intent into concrete Kubernetes objects.
