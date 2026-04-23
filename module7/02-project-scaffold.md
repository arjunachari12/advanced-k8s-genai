# Exercise 2: Scaffold the Operator Project

This repository already includes a working operator project, so this exercise is mainly a walkthrough of how the checked-in codebase was originally generated.

Do not rerun these scaffold commands inside the committed `module7` folder unless you intentionally want to overwrite generated project files.

## Move Into the Module Directory

```bash
cd module7
export PATH="$HOME/.local/bin:$HOME/.local/lib/go-toolchain/go/bin:$PATH"
```

## Recreate the Scaffold From Scratch

These are the commands used to create the project:

```bash
operator-sdk init \
  --domain workshop.io \
  --repo github.com/arjun/genai-k8s/module7/ai-workload-operator \
  --project-name ai-workload-operator \
  --plugins go/v4

operator-sdk create api \
  --group ai \
  --version v1alpha1 \
  --kind AIApp \
  --resource \
  --controller \
  --make
```

You do not need to rerun those commands now because the generated project is already in place.

If you want a safe hands-on version that creates a brand-new disposable operator project, use `02a-create-a-fresh-operator-project.md` instead.

## Inspect the Important Files

```bash
find . -maxdepth 2 -type f | sort
```

Focus on these paths:

- `api/v1alpha1/aiapp_types.go`
- `internal/controller/aiapp_controller.go`
- `cmd/main.go`
- `config/crd/`
- `config/samples/`
- `Makefile`

## What Just Happened?

Operator SDK generated a standard controller-runtime project. That scaffold gives you a CRD, API types, controller wiring, RBAC manifests, and Make targets so you can focus on business logic rather than bootstrapping everything by hand.
