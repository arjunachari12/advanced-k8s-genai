# Exercise 3: Create and Register the CRD

In this exercise, you will inspect the custom resource type and generate the CRD that Kubernetes will register.

## Review the API Type

Open the API definition:

`api/v1alpha1/aiapp_types.go`

The `AIAppSpec` describes the desired state:

- `image`
- `replicas`
- `port`
- `serviceType`
- `modelName`
- `llmUrl`
- `logLevel`

The `AIAppStatus` describes the observed state:

- `phase`
- `readyReplicas`
- `deploymentName`
- `serviceName`
- `conditions`

## Generate CRD Manifests

```bash
cd module7
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"

make manifests generate
```

Review the generated CRD:

```bash
sed -n '1,220p' config/crd/bases/ai.workshop.io_aiapps.yaml
```

## Install the CRD in the Cluster

```bash
make install
```

Verify registration:

```bash
kubectl get crd aiapps.ai.workshop.io
kubectl api-resources | grep aiapp
```

Expected output includes:

```text
aiapps   ai.workshop.io/v1alpha1   true   AIApp
```

## What Just Happened?

You extended the Kubernetes API with a new namespaced resource named `AIApp`. Once the CRD is installed, Kubernetes accepts objects of that type just like it accepts `Deployment` or `Service` objects.
