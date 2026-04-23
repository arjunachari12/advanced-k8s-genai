# Exercise 1: Use kubectl-ai for Kubernetes Help

This exercise introduces `kubectl-ai` as the fastest way to show students what AI-assisted Kubernetes workflows feel like.

## What You Are Doing

You are not building any backend yet. You are using an existing AI tool that turns natural-language requests into Kubernetes guidance.

This is useful because students can immediately see value from AI in areas like:

- generating starter manifests
- explaining YAML
- suggesting troubleshooting steps

## Why Start Here?

Starting with `kubectl-ai` gives students a clear baseline:

- what AI can do with prompts alone
- what still depends on the user reviewing and validating the output

That baseline makes the second half of the module easier to understand, because students can then compare prompt-only help with tool-backed help through MCP.

## Prerequisites

- `kubectl` works against your cluster
- internet access is available for plugin installation
- you have an LLM provider key, such as `OPENAI_API_KEY`

## Install Krew If Needed

```bash
(
  set -x
  cd "$(mktemp -d)"
  OS="$(uname | tr '[:upper:]' '[:lower:]')"
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
  KREW="krew-${OS}_${ARCH}"
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${KREW}.tar.gz"
  tar zxvf "${KREW}.tar.gz"
  ./"${KREW}" install krew
)
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
```

## Install kubectl-ai

```bash
kubectl krew install ai
```

Verify:

```bash
kubectl ai --help
```

## Configure Your Provider

Example with OpenAI:

```bash
export OPENAI_API_KEY="<your-key>"
```

## Try Manifest Generation

Run:

```bash
kubectl ai "create an nginx deployment with 3 replicas"
kubectl ai "create a redis deployment and expose it internally on port 6379"
```

Do not blindly apply the output. Review it first.

Ask students questions like:

- Did the generated YAML include the namespace you expected?
- Did it expose the right port?
- Would you apply it as-is in production?

## Try Explanation and Troubleshooting Prompts

Examples:

```bash
kubectl ai "explain what a readiness probe does in Kubernetes"
kubectl ai "how do I inspect why a pod is in CrashLoopBackOff?"
```

## What Just Happened?

You used AI as a Kubernetes copilot. It can speed up drafting, explanation, and discovery, but it still depends on the user to verify output and supply the right context.

In the next exercise, you will build a read-only MCP server so AI tooling can inspect real cluster state instead of relying only on prompts.
