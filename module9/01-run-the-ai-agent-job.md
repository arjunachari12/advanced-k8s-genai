# Exercise 1: Run the AI Agent as a Kubernetes Job

This is the main lab for Module 9.

## What You Are Building

You are building and running an in-cluster AI operations assistant.

The assistant:

- runs as a Kubernetes Job
- calls read-only cluster tools through MCP
- uses Ollama for summarization
- prints a diagnosis to the Job logs

## Why This Matters

This is the first time in the course that the AI workflow itself becomes a Kubernetes workload.

That matters because it shows how AI operations can be packaged the same way platform teams package any other automation:

- as a container image
- with environment variables
- with service dependencies
- with logs and runtime state visible in Kubernetes

## How The Agent Works

At a high level, `ai-agent/agent.py` does this:

1. fetch pods from the `genai` namespace through MCP
2. decide which pod looks most unhealthy
3. fetch recent events
4. optionally fetch logs if the failure looks like a runtime problem
5. ask Ollama to produce a short diagnosis and next step

This means the agent is not just calling the model once. It is following a small decision graph.

## Step 1: Review the Main Files

Open:

- `module9/ai-agent/agent.py`
- `module9/ai-agent/k8s/job.yaml`
- `module9/ai-agent/k8s/ollama.yaml`

Pay attention to:

- `MCP_SERVER_URL`
- `OLLAMA_BASE_URL`
- `TARGET_NAMESPACE`
- the prompt passed through `ASSISTANT_PROMPT`

## Step 2: Build and Load the Agent Image

```bash
docker build -t ai-k8s-assistant:0.1.0 module9/ai-agent
kind load docker-image ai-k8s-assistant:0.1.0 --name multi-node-cluster
```

## Step 3: Deploy or Verify Ollama

```bash
kubectl apply -f module9/ai-agent/k8s/ollama.yaml
kubectl rollout status deployment/ollama -n genai --timeout=600s
```

If the MCP server from Module 8 is not already running, deploy that first before continuing.

## Step 4: Create a Failure for the Agent to Diagnose

```bash
kubectl create deployment broken-redis \
  --image=redis:this-tag-does-not-exist \
  -n genai \
  --dry-run=client -o yaml | kubectl apply -f -
```

Verify the failure:

```bash
kubectl get pods -n genai
```

Expected state:

- one `broken-redis` pod enters `ErrImagePull` or `ImagePullBackOff`

## Step 5: Run the Agent Job

```bash
kubectl delete job ai-k8s-assistant -n genai --ignore-not-found
kubectl apply -f module9/ai-agent/k8s/job.yaml
kubectl wait --for=condition=complete job/ai-k8s-assistant -n genai --timeout=300s
```

## Step 6: Read the Diagnosis

```bash
kubectl logs -n genai job/ai-k8s-assistant
```

Students should look for:

- which MCP tools were used
- which pod was selected as unhealthy
- whether logs were needed or skipped
- the final diagnosis
- the exact next `kubectl` command suggested by the agent

## What Just Happened?

You ran an agent as a Kubernetes Job.

The agent used real cluster context, not just a prompt. It observed the namespace, chose what to inspect, and then produced a remediation-oriented summary.
