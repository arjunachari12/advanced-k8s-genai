# Module 1: Environment Setup and Cluster Bootstrapping

Module 1 prepares the workstation and creates the local Kubernetes cluster used by the rest of the course.

## Learning Objectives

By the end of this module, students should be able to:

1. verify Docker, `kubectl`, `kind`, and Helm are installed
2. create a multi-node KIND cluster
3. confirm the Kubernetes context is healthy
4. understand the repo layout they will use in later modules

## Architecture / Flow

The workshop uses a single local KIND cluster with:

- 1 control-plane node
- 2 worker nodes
- the `kind-multi-node-cluster` context

That cluster becomes the runtime for all later modules.

## Assets In This Module

- `kind-config.yaml` - KIND cluster definition with one control plane and two workers

## Prerequisites

- Docker installed and running
- `kubectl` installed
- `kind` installed
- `helm` installed

Quick host validation:

```bash
docker version
kubectl version --client
kind version
helm version
./scripts/verify-env.sh
```

## Step 1: Create the Cluster

From the repository root:

```bash
cd module1
kind create cluster --name multi-node-cluster --config kind-config.yaml
```

## Step 2: Verify Cluster Health and Context

```bash
kubectl cluster-info --context kind-multi-node-cluster
kubectl get nodes -o wide
kubectl get pods -A
```

Expected result:

- 3 nodes total
- 1 control-plane node
- 2 worker nodes
- core system pods in `kube-system` moving to `Running`

## Step 3: Confirm the Training Repo Layout

From the repository root:

```bash
find module1 module2 module3 module4 module5 module6 module7 module8 module9 -maxdepth 1 -type f -name README.md | sort
```

This shows the module-by-module structure students will follow for the rest of the workshop.

## Validation Checks

```bash
kubectl config current-context
kubectl get nodes
docker ps
```

Instructor checklist:

- current context is `kind-multi-node-cluster`
- all 3 nodes are `Ready`
- Docker and `kubectl` commands run without permission errors

## Troubleshooting

- If `kubectl cluster-info` fails, confirm Docker or Rancher Desktop is running.
- If the current context points to `kind-multi-node-cluster` but the API server is unreachable, delete and recreate the cluster.
- If image pulls fail later in the workshop, verify local network access before moving past Module 1.

## Cleanup

If you need to recreate the cluster later:

```bash
kind delete cluster --name multi-node-cluster
```

## Exit Criteria

Students are ready for Module 2 when:

- `kubectl get nodes` shows all nodes as `Ready`
- the current context is `kind-multi-node-cluster`
- Docker can build images locally
