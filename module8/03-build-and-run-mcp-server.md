# Exercise 3: Build and Run a Read-Only Kubernetes MCP Server

This exercise is the core of Module 8.

You will build, deploy, and use a small MCP server that exposes real Kubernetes data through a tightly scoped read-only interface.

## What You Are Building

You are building a Python MCP server for Kubernetes.

The server exposes a few tools:

- `get_cluster_nodes`
- `get_namespaces`
- `get_pods_in_namespace`
- `get_recent_events`
- `get_pod_logs`

These tools are backed by the Kubernetes API, but the RBAC only allows read operations.

## Why Build This?

This is the bridge between AI and real infrastructure.

Instead of giving an AI assistant unrestricted access to a cluster, you can expose only a small, audited set of capabilities. That is the main idea students should take away from this lab.

This design gives you:

- live cluster context
- safer boundaries
- predictable tool behavior
- a reusable pattern for future platform tooling

## Step 1: Review the Server and RBAC

Open these files first:

- `module8/mcp-server/server.py`
- `module8/mcp-server/k8s/rbac.yaml`
- `module8/mcp-server/k8s/deployment.yaml`

Notice two important things:

- the server only exposes read-oriented helper tools
- the ClusterRole only uses `get`, `list`, and `watch`

## Step 2: Build the MCP Server Image

```bash
docker build -t mcp-k8s-server:0.1.0 module8/mcp-server
```

## Step 3: Load the Image into KIND

```bash
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
```

## Step 4: Deploy the MCP Server

```bash
kubectl apply -f module8/mcp-server/k8s/rbac.yaml
kubectl apply -f module8/mcp-server/k8s/deployment.yaml
kubectl rollout status deployment/mcp-server -n genai
```

Verify the pod:

```bash
kubectl get pods -n genai -l app=mcp-server -o wide
kubectl logs -n genai deploy/mcp-server --tail=30
```

## Step 5: Port-Forward the Service

Keep this running in one terminal:

```bash
kubectl port-forward -n genai svc/mcp-server-svc 8000:80
```

The SSE endpoint is:

```text
http://127.0.0.1:8000/sse
```

## Step 6: Test the MCP Tools from Your Laptop

In another terminal:

```bash
python3 -m pip install --user -r module8/mcp-server/requirements.txt
python3 module8/mcp-server/client.py
```

You should see:

- a successful client connection
- the list of available tools
- live cluster data returned from tool calls

## Step 7: Run a Simple Troubleshooting Scenario

Create a broken deployment:

```bash
kubectl create deployment broken-app \
  --image=nginx:non-existent-tag \
  -n genai
```

Now use your AI tooling with cluster context to investigate. Prompts can include:

- "Why is `broken-app` not starting in namespace `genai`?"
- "Show the likely root cause and the next kubectl command I should run."

Clean it up after:

```bash
kubectl delete deployment broken-app -n genai
```

## What Just Happened?

You deployed your own tool-backed integration point between AI and Kubernetes.

This is more powerful than prompt-only AI because the assistant can inspect real cluster state. It is also safer than broad direct access because the server only exposes a controlled read-only surface.
