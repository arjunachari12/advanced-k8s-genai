# Kubernetes MCP Server

This example exposes a few **read-only Kubernetes tools** over MCP so an AI assistant can inspect cluster state safely.

This folder is the implementation used by `../02-build-and-run-mcp-server.md`.

## What This Code Does

This code is a small Python service that sits between an AI client and the Kubernetes API.

Its job is simple:

1. connect to Kubernetes
2. expose a small set of safe MCP tools
3. return cluster information in structured text

You can think of it as a controlled adapter layer. Instead of letting an AI tool run arbitrary `kubectl` commands, we expose a few approved operations through named functions.

## Why This Is Useful for Platform and DevOps Work

For cloud and platform teams, the important idea is not the Python syntax. The important idea is the control point.

This pattern gives you:

- a fixed list of allowed actions
- a clear RBAC boundary
- predictable outputs for AI-assisted troubleshooting
- an auditable place to add or remove capabilities

In other words, this server is less about "building an app" and more about "publishing a safe operational interface."

## Tools

- `get_cluster_nodes`
- `get_namespaces`
- `get_pods_in_namespace`
- `get_recent_events`
- `get_pod_logs`

## How The Server Works

At a high level, `server.py` does four things:

### 1. Load Kubernetes credentials

The server first tries to load in-cluster credentials.

That is what it uses when running inside Kubernetes as a pod.

If that is not available, it falls back to the local `kubeconfig`.

That is what makes the same code work both:

- inside the cluster
- on your laptop during local testing

### 2. Create a Kubernetes API client

After loading credentials, it creates a `CoreV1Api` client from the Kubernetes Python SDK.

That client is what the tool functions use to talk to the cluster.

### 3. Register MCP tools

Each function decorated with `@mcp.tool()` becomes a tool an AI client can call.

Examples:

- `get_cluster_nodes()` lists node readiness and kubelet versions
- `get_namespaces()` returns all namespaces
- `get_pods_in_namespace()` returns pod status, images, nodes, and container states
- `get_recent_events()` returns recent Kubernetes events
- `get_pod_logs()` reads pod logs for troubleshooting

### 4. Serve the tools over SSE

At the bottom of the file, the service starts a FastMCP server and exposes it over HTTP using SSE transport.

That is why the endpoint is:

```text
http://localhost:8000/sse
```

An MCP client connects to that endpoint, discovers available tools, and calls them as needed.

## What Students Should Notice in the Code

If students open `server.py`, these are the main ideas to focus on:

- `load_kube_config()` shows how the same service works locally and in-cluster
- `core_v1 = client.CoreV1Api()` is the Kubernetes API entry point
- `@mcp.tool()` marks which functions are exposed to AI clients
- each tool returns formatted JSON text instead of raw Python objects
- the server does not contain any write operations such as create, patch, update, or delete

## Why The Output Is JSON Text

The tools return formatted JSON strings because that is easy for both humans and AI systems to read.

For operations teams, this also has a practical benefit:

- the output is structured
- it is easy to inspect during demos
- it is predictable for troubleshooting prompts

## How RBAC and Code Work Together

The Python code defines what the server tries to do.

The Kubernetes RBAC defines what the server is allowed to do.

Both matter.

Even if someone changed the code later, the service account in `k8s/rbac.yaml` is still limited to read-only actions on:

- nodes
- namespaces
- pods
- events
- pod logs

That is an important platform design lesson: do not rely only on application logic for safety. Enforce the boundary in Kubernetes too.

## Local Run

```bash
cd module8/mcp-server
python3 -m pip install --user -r requirements.txt
python server.py
```

The SSE endpoint is:

```text
http://localhost:8000/sse
```

To test the server from another terminal:

```bash
python3 client.py
```

## Build and Deploy to Kind

```bash
docker build -t mcp-k8s-server:0.1.0 .
kind load docker-image mcp-k8s-server:0.1.0 --name multi-node-cluster
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/mcp-server -n genai
kubectl port-forward -n genai svc/mcp-server-svc 8000:80
python3 client.py
```

## Why The RBAC Is Important

The Kubernetes access in `k8s/rbac.yaml` is intentionally read-only.

That is the point of the example:

- the AI assistant can inspect the cluster
- the MCP server cannot create, patch, or delete workloads

This makes the lab safer and gives students a concrete example of how to expose useful AI tools without granting broad write privileges.
