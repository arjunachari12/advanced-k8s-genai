# Exercise 2A: Create a Fresh Operator Project

Use this optional exercise if you want to run the scaffold commands yourself in a scratch directory.

This does not modify the committed `module7` project. It creates a separate disposable operator project you can inspect and delete afterward.

## Create a Scratch Workspace

```bash
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"

mkdir -p /tmp/module7-operator-lab
cd /tmp/module7-operator-lab
rm -rf ai-workload-operator-scratch
mkdir ai-workload-operator-scratch
cd ai-workload-operator-scratch
```

## Initialize the Operator SDK Project

```bash
operator-sdk init \
  --domain workshop.io \
  --repo github.com/arjun/genai-k8s/module7/ai-workload-operator-scratch \
  --project-name ai-workload-operator-scratch \
  --plugins go/v4
```

## Create the `AIApp` API and Controller

```bash
operator-sdk create api \
  --group ai \
  --version v1alpha1 \
  --kind AIApp \
  --resource \
  --controller \
  --make
```

## Generate the CRD and Supporting Code

```bash
make manifests generate
```

## Inspect the Generated Project

```bash
find . -maxdepth 2 -type f | sort
```

Pay attention to:

- `api/v1alpha1/aiapp_types.go`
- `internal/controller/aiapp_controller.go`
- `cmd/main.go`
- `config/crd/`
- `config/samples/`
- `Makefile`

## Compare It With the Real Lab Project

When you are done exploring the scratch scaffold, return to the committed module:

```bash
cd /home/arjun/advanced-k8s-genai/module7
```

The checked-in `module7` project already includes the custom API fields, controller logic, samples, and tests used in the rest of this lab.

## What Just Happened?

You created a brand-new Operator SDK project and generated the first version of the `AIApp` CRD, API types, controller, RBAC manifests, and Make targets. This is the baseline scaffold that the committed lab project builds on.
