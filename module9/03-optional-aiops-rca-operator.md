# Exercise 3: Optional AIOps RCA Operator

Use this exercise as an advanced extension, not the primary student lab.

## What You Are Building

This pattern wraps AI-assisted troubleshooting in a Custom Resource Definition and operator workflow.

Instead of launching a Job directly, a user creates an `RCARequest` custom resource. The operator watches that resource, runs a LangGraph-based investigation flow, and writes the result back into status.

## Why This Matters

This pattern is useful for platform engineering discussions because it shows how AI workflows can become first-class Kubernetes APIs.

That means teams can model AI operations as:

- declarative requests
- reconciled workflows
- status-driven results

It is conceptually similar to Module 7, but now the controller logic is an AI-assisted RCA workflow instead of a normal application reconciler.

## Main Files

Open:

- `module9/aiops-rca-operator/crd.yaml`
- `module9/aiops-rca-operator/operator.py`
- `module9/aiops-rca-operator/graph.py`
- `module9/aiops-rca-operator/sample.yaml`

## How It Works

1. `crd.yaml` defines the `RCARequest` custom resource
2. `operator.py` watches for new `RCARequest` objects
3. `graph.py` chains planner, debugger, analyzer, and fixer steps
4. the operator writes `analysis` and `fix` into the resource status

## Validation Level

This extension was syntax-checked and instructor-validated locally against the shared KIND cluster.

That said, it is still best treated as:

- an instructor extension
- an advanced stretch lab
- a design-pattern discussion for teams exploring CRD-driven AI operations

## Basic Walkthrough

Install dependencies:

```bash
cd module9/aiops-rca-operator
python3 -m pip install --user -r requirements.txt
```

Apply the CRD:

```bash
kubectl apply -f crd.yaml
```

Run the operator locally:

```bash
cd module9/aiops-rca-operator
kopf run operator.py --verbose
```

In another terminal, pick a real pod name to investigate:

```bash
kubectl get pods -n genai
```

Update `sample.yaml` so `spec.podName` matches a real pod, then create a request:

```bash
kubectl apply -f sample.yaml
kubectl get rcarequest sample-rca -n genai -o yaml
```

If you want model-backed plan or fix generation when running the operator locally on your laptop, port-forward Ollama and set:

```bash
kubectl port-forward -n genai svc/ollama 11434:11434
export OLLAMA_BASE_URL="http://127.0.0.1:11434"
```

For common Kubernetes failure modes such as image pull errors, the operator can still produce deterministic fixes even without Ollama connectivity.

## What Just Happened?

You moved from “run an AI worker” to “declare an AI troubleshooting request as a Kubernetes object.”

That is a useful architectural pattern for advanced platform teams, even if it is more complex than the primary Job-based lab.
