# GenAI Kubernetes Training Repo

This repository contains the hands-on assets for a 3-day Kubernetes and GenAI workshop. The repo is organized by training module so students can move through the course in sequence without having to hunt for alternate or outdated paths.

## Course Overview

The workshop teaches students how to:

1. create a local Kubernetes environment with KIND
2. deploy a simple GenAI application with raw YAML
3. add observability with Prometheus, Loki, and Grafana
4. package the platform as a Helm chart
5. extend the platform with autoscaling, GitOps, operators, MCP, and agent workflows

## Global Prerequisites

- Docker Desktop or Rancher Desktop
- `kubectl`
- `kind`
- `helm`
- `git`
- `make`
- Python 3.11+

Recommended laptop baseline:

- 4 CPU or more
- 8 GB RAM minimum
- enough free disk for container images and Ollama models

## Repo Structure

```text
.
├── module1/
├── module2/
├── module3/
├── module4/
├── module5/
├── module6/
├── module7/
├── module8/
├── module9/
├── scripts/
├── Makefile
└── training-agenda.txt
```

Each `moduleN/` folder contains:

- `README.md`
- module-specific code, manifests, or scripts
- validation and cleanup guidance

## Suggested Delivery Order

Day 1

1. [module1](./module1/README.md) - Environment setup and cluster bootstrapping
2. [module2](./module2/README.md) - Manual deployment with Kubernetes YAML
3. [module3](./module3/README.md) - Observability with Prometheus, Loki, and Grafana
4. [module5](./module5/README.md) - Helm chart development

Day 2

5. [module4](./module4/README.md) - Autoscaling with KEDA and Prometheus metrics
6. [module6](./module6/README.md) - GitOps and progressive delivery with ArgoCD
7. [module7](./module7/README.md) - CRDs and Kubernetes operators

Day 3

8. [module8](./module8/README.md) - AI-augmented Kubernetes with kubectl-ai and MCP
9. [module9](./module9/README.md) - Agentic AI systems on Kubernetes

## Module Dependency Map

- `module1` is the base for the whole course.
- `module2` depends on `module1`.
- `module3` depends on `module2`.
- `module5` depends on `module2` and benefits from `module3`.
- `module4` depends on `module5`.
- `module6` depends on `module5` and uses monitoring concepts from `module3`.
- `module7` depends on `module1` and can be taught after `module6`.
- `module8` depends on a working cluster and benefits from `module2` and `module3`.
- `module9` depends on `module8`.

## Student Progression

Students should:

1. complete each module in order unless the instructor explicitly skips one
2. keep the same local KIND cluster across modules where practical
3. use the validation and cleanup sections at the end of each module
4. return to the repo root before switching modules

## Setup

From the repository root:

```bash
pwd
make validate
./scripts/verify-env.sh
```

The environment verifier checks local tools and reports whether the Kubernetes API is reachable from the current context.

## Validation

Before class, run:

```bash
make validate
make clean-python-cache
```

This validates:

- Python syntax for the training services and agents
- the Helm chart in `module5/chart`
- the Docker Compose setups in `module2` and `module8`

## Notes For Instructors

- Some live Kubernetes validations require a running KIND cluster. If the context exists but the API server is down, `kubectl apply`, `kubectl get`, and `kubectl wait` will fail until the cluster is recreated.
- `module8/local-mcp-ollama/ollama_data/` is ignored because it is local runtime state, not training source code.
