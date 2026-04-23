# Module 7: CRDs and Kubernetes Operators

This module uses a real Go operator project so students can move from Kubernetes theory to a working controller.

## What We Are Building

The sample custom resource in this module is `AIApp`.

`AIApp` is a higher-level application object for the GenAI API workload used in earlier modules. Instead of asking users to hand-author a `Deployment`, `Service`, probes, labels, and environment variables every time, the module lets them define one Kubernetes-native object that describes the app they want to run.

An `AIApp` can express things like:

- which container image to run
- how many replicas to create
- which model name to pass into the workload
- which internal LLM endpoint the app should call
- how the service should be exposed

The controller then translates that intent into the lower-level Kubernetes resources required to run the workload safely.

The custom resource is named `AIApp`. Each `AIApp` object manages:

- one `Deployment`
- one `Service`
- status conditions that report reconciliation progress

## Why Build This As A CRD?

This workload is a good CRD example because it has repeated operational rules that are easy to get wrong when written by hand.

Without a CRD, every team or student would need to remember:

- the right container image and port
- the expected environment variables like `MODEL_NAME` and `LLM_URL`
- the probe configuration
- the labels and selectors that keep the `Deployment` and `Service` connected
- how to inspect readiness and rollout state across multiple objects

By defining `AIApp` as a custom resource, we move those rules into the platform itself. Users describe the application they want, and the controller consistently creates the correct Kubernetes objects.

## Benefits Of Using A CRD And Operator

- Simpler user experience: students create one `AIApp` instead of assembling several YAML resources by hand.
- Safer defaults: the controller can inject known-good defaults for ports, log level, service type, and model wiring.
- Consistency: every deployed app follows the same labeling, service, and health-check patterns.
- Reconciliation: if a managed `Deployment` or `Service` drifts, the controller notices and repairs it.
- Better status reporting: the custom resource can expose app-specific status like `phase`, `readyReplicas`, `deploymentName`, and `serviceName`.
- Platform abstraction: application users work with business intent, while the operator handles Kubernetes implementation details.
- Reuse: once the pattern is in code, every future `AIApp` benefits from the same automation.

## Learning Outcomes

Students will learn how to:

1. install the local toolchain required for Go-based operators
2. register a CRD with the Kubernetes API
3. build a controller using Operator SDK
4. reconcile desired state into Kubernetes resources
5. automate lifecycle management for an AI API workload
6. inspect status, events, and spec changes during reconciliation

## Architecture / Flow

- students define an `AIApp` custom resource
- the controller watches `AIApp` objects
- reconciliation creates or updates a Deployment and Service
- status conditions report controller progress

## Module Flow

1. `01-prerequisites.md`
2. `02-project-scaffold.md`
3. `02a-create-a-fresh-operator-project.md` (optional scratch exercise)
4. `03-create-the-crd.md`
5. `04-build-the-controller.md`
6. `05-run-the-operator.md`
7. `06-create-custom-resources.md`
8. `07-reconciliation-patterns.md`
9. `08-cleanup.md`

## Lab Code

The working operator project for this module lives in this same directory:

- `api/v1alpha1/aiapp_types.go`
- `internal/controller/aiapp_controller.go`
- `config/samples/ai_v1alpha1_aiapp.yaml`
- `config/samples/ai_v1alpha1_aiapp_minimal.yaml`

If students want to practice scaffolding from zero, use `02a-create-a-fresh-operator-project.md` in a temporary directory, then return to this committed module for the rest of the exercises.

## Tested Commands

The module was validated on the shared KIND cluster with:

```bash
export PATH="$HOME/.local/bin:$HOME/.local/lib/go-toolchain/go/bin:$PATH"

make build
make test
make install
make run
kubectl apply -f config/samples/ai_v1alpha1_aiapp.yaml
kubectl patch aiapp aiapp-sample -n ai-operators-lab --type merge -p '{"spec":{"replicas":2}}'
```

## Quick Start

If you want to jump straight to the runnable lab:

```bash
cd module7
export PATH="$HOME/.local/bin:$HOME/.local/lib/go-toolchain/go/bin:$PATH"

kubectl create namespace ai-operators-lab --dry-run=client -o yaml | kubectl apply -f -
make build
make test
make install
make run
```

In a second terminal:

```bash
kubectl apply -f config/samples/ai_v1alpha1_aiapp.yaml
kubectl get aiapp -n ai-operators-lab
kubectl get deployment,svc,pods -n ai-operators-lab
```

## Troubleshooting

- If `make build` fails, verify that `go` and `operator-sdk` are on your `PATH`.
- If `make test` fails, run `make setup-envtest` once and then retry.
- If `make run` starts but nothing reconciles, confirm the CRD is installed with `make install`.
- If resources are not created, inspect controller logs in the terminal running `make run`.

## Cleanup

See `08-cleanup.md`, or run:

```bash
kubectl delete namespace ai-operators-lab --ignore-not-found
```

## Instructor Validation Checklist

- students can install the CRD
- the controller starts with `make run`
- applying an `AIApp` creates a Deployment and Service
