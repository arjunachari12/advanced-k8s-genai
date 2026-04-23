# Helm Artifact Hub and Templating Guide

This guide gives students extra Helm practice beyond the main `genai` chart in Module 5.

It covers:

- how to discover useful charts from Artifact Hub
- how to inspect a chart before installing it
- how to install and uninstall a public chart
- how to create a small chart from scratch with templating
- how to upgrade a chart and verify a visible change

## Why Use Artifact Hub

Artifact Hub is the easiest place to discover popular Helm charts, review chart metadata, and check whether a chart looks production-ready before installing it.

Useful Artifact Hub examples to browse:

- `bitnami/nginx`: https://artifacthub.io/packages/helm/bitnami/nginx
- `bitnami/redis`: https://artifacthub.io/packages/helm/bitnami/redis
- `ingress-nginx/ingress-nginx`: https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx
- `prometheus-community/kube-prometheus-stack`: https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack

As of April 23, 2026, these were good teaching examples because they represent common Helm use cases:

- `nginx` for a simple web workload
- `redis` for a stateful application
- `ingress-nginx` for cluster ingress
- `kube-prometheus-stack` for a large multi-component platform chart

## Step 1: Add Repositories and Inspect Charts

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Good discovery commands:

```bash
helm search repo bitnami/nginx
helm search repo bitnami/redis
helm show chart bitnami/nginx
helm show values bitnami/nginx | head -n 40
helm show chart ingress-nginx/ingress-nginx
helm show chart prometheus-community/kube-prometheus-stack
```

Teaching point:

- `helm show chart` tells students what the chart is
- `helm show values` shows which knobs they can tune
- `helm template` lets them inspect output before any install

## Step 2: Template a Heavier Chart Before Installing It

For larger charts, teach students to render first before installing.

Example with Redis:

```bash
helm template demo-redis bitnami/redis \
  --namespace module5-lab \
  --set architecture=standalone \
  --set auth.enabled=false \
  --set master.persistence.enabled=false \
  --set replica.replicaCount=0
```

In this repo, that command rendered cleanly and produced a multi-resource manifest.

Good examples to inspect but not blindly install in a training cluster:

- `prometheus-community/kube-prometheus-stack`
- `ingress-nginx/ingress-nginx`

Why:

- they create many resources
- they may introduce CRDs, admission webhooks, or cluster-wide components
- they are best installed after students understand what they are adding

## Step 3: Install and Uninstall a Lightweight Public Chart

The most reliable public example tested in this environment was `bitnami/nginx`.

Install it into a disposable namespace:

```bash
helm install ah-nginx bitnami/nginx \
  -n module5-lab \
  --create-namespace \
  --set service.type=ClusterIP
```

Validate it:

```bash
helm status ah-nginx -n module5-lab
kubectl get pods,svc -n module5-lab
kubectl -n module5-lab port-forward svc/ah-nginx 28080:80
```

Open `http://127.0.0.1:28080` and confirm the default NGINX page loads.

Uninstall it:

```bash
helm uninstall ah-nginx -n module5-lab
```

## Step 4: Create a New Chart

This repo includes a small teaching chart at `module5/starter-chart`.

It was scaffolded from:

```bash
helm create module5/starter-chart
```

Then simplified into a small example that shows visible templating through a web page.

Important files to study:

- `starter-chart/Chart.yaml`
- `starter-chart/values.yaml`
- `starter-chart/templates/configmap.yaml`
- `starter-chart/templates/deployment.yaml`
- `starter-chart/templates/service.yaml`

What this chart teaches:

- values in `values.yaml` drive the page content
- the `ConfigMap` template renders HTML using Helm values
- the `Deployment` mounts that HTML into NGINX
- a checksum annotation on the pod template forces a rollout when the page config changes

## Step 5: Lint and Render the Starter Chart

```bash
helm lint module5/starter-chart

helm template starter-demo module5/starter-chart \
  -n module5-lab
```

Students should inspect the rendered output and find:

- the rendered HTML inside the `ConfigMap`
- the `Deployment`
- the `Service`
- the checksum annotation that triggers rollouts on config changes

## Step 6: Install the Starter Chart

```bash
helm upgrade --install starter-demo module5/starter-chart -n module5-lab
```

Validate it:

```bash
helm status starter-demo -n module5-lab
kubectl get pods,svc -n module5-lab
kubectl -n module5-lab port-forward svc/starter-demo-starter-chart 28081:80
```

Open `http://127.0.0.1:28081`.

Students should see a simple page rendered from Helm values.

## Step 7: Upgrade the Chart and Watch the Page Change

Run:

```bash
helm upgrade starter-demo module5/starter-chart \
  -n module5-lab \
  --set page.heading="Checksum Rollout Works" \
  --set page.message="Config changes now trigger a fresh rollout."
```

Then review:

```bash
helm history starter-demo -n module5-lab
kubectl rollout status deployment/starter-demo-starter-chart -n module5-lab
```

Refresh `http://127.0.0.1:28081`.

Students should see the page update with the new heading and message.

## Step 8: Run a Helm Test

The starter chart includes a simple Helm test hook.

Run:

```bash
helm test starter-demo -n module5-lab
```

This is useful for teaching that charts can define post-install or post-upgrade validation logic.

## Step 9: Uninstall and Clean Up

Remove the starter chart:

```bash
helm uninstall starter-demo -n module5-lab
```

If the namespace was only used for this lab:

```bash
helm uninstall ah-nginx -n module5-lab || true
helm uninstall ah-apache -n module5-lab || true
kubectl delete namespace module5-lab --ignore-not-found
```

## Notes From This Environment

The following workflows were tested successfully in this repository and cluster:

- `helm repo update`
- `helm show chart` for `bitnami/nginx`, `ingress-nginx/ingress-nginx`, and `prometheus-community/kube-prometheus-stack`
- `helm template` for `bitnami/redis`
- `helm install`, `helm status`, and HTTP validation for `bitnami/nginx`
- `helm create`, `helm lint`, `helm template`, `helm upgrade --install`, `helm upgrade`, `helm history`, `helm test`, and HTTP validation for `module5/starter-chart`

One chart install was intentionally not recommended as a primary example here:

- `bitnami/apache` installed as a Helm release, but the workload hit `ImagePullBackOff` in this environment because the referenced image tag could not be pulled

That is a good teaching reminder:

- always inspect chart values
- always test in a non-production namespace first
- do not assume every public chart will work unchanged in every environment
