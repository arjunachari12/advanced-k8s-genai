# Exercise 2: Use kubectl-ai for Kubernetes Help

This exercise introduces `kubectl-ai` as the fastest way to show students what AI-assisted Kubernetes workflows feel like.

## What You Are Doing

You are not building any backend yet. You are using an existing AI tool that turns natural-language requests into Kubernetes guidance.

This is useful because students can immediately see value from AI in areas like:

- generating starter manifests
- explaining YAML
- suggesting troubleshooting steps

## Why This Comes Second?

After the local Ollama setup, students already have a working AI endpoint. That makes this exercise easier to demo because you can start with the local model and then optionally compare it with Gemini or OpenAI.

`kubectl-ai` gives students a clear baseline:

- what AI can do with prompts alone
- what still depends on the user reviewing and validating the output

That baseline makes the second half of the module easier to understand, because students can then compare prompt-only help with tool-backed help through MCP.

## Prerequisites

- `kubectl` works against your cluster
- internet access is available for plugin installation
- you have an LLM provider key, such as `OPENAI_API_KEY` or `GEMINI_API_KEY`

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

If you completed Exercise 1, you can use the local Ollama bridge first:

```bash
export KUBECTL_AI_PROVIDER="openai"
export OPENAI_API_BASE="http://localhost:8888/v1"
export OPENAI_API_KEY="local"
kubectl ai --llm-provider openai --model tinyllama "create an nginx deployment with 3 replicas"
```

You can also use a hosted provider.

Example with OpenAI:

```bash
export OPENAI_API_KEY="<your-openai-key>"
printenv OPENAI_API_KEY
```

Important:

- `kubectl ai` defaults to `--llm-provider gemini`
- `kubectl ai` also defaults to the Gemini model `gemini-2.5-pro`
- if you only set `OPENAI_API_KEY`, you must also pass `--llm-provider openai`
- when using OpenAI, you should also pass an OpenAI model explicitly, such as `--model gpt-4o-mini`
- otherwise the tool still looks for `GEMINI_API_KEY`

If you want to use Gemini instead, export `GEMINI_API_KEY` and keep the default provider.

Example with Gemini:

```bash
export GEMINI_API_KEY="<your-gemini-key>"
printenv GEMINI_API_KEY
```

Then run either:

```bash
kubectl ai "create an nginx deployment with 3 replicas"
```

or explicitly:

```bash
kubectl ai --llm-provider gemini --model gemini-2.5-pro "create an nginx deployment with 3 replicas"
```

## Try Manifest Generation

Run:

```bash
kubectl ai --llm-provider openai --model gpt-4o-mini "create an nginx deployment with 3 replicas"
kubectl ai --llm-provider openai --model gpt-4o-mini "create a redis deployment and expose it internally on port 6379"
```

Do not blindly apply the output. Review it first.

Ask students questions like:

- Did the generated YAML include the namespace you expected?
- Did it expose the right port?
- Would you apply it as-is in production?

## Try Explanation and Troubleshooting Prompts

Examples:

```bash
kubectl ai --llm-provider openai --model gpt-4o-mini "explain what a readiness probe does in Kubernetes"
kubectl ai --llm-provider openai --model gpt-4o-mini "how do I inspect why a pod is in CrashLoopBackOff?"
```

If you still get a provider error, run:

```bash
kubectl ai --llm-provider openai --help
kubectl ai --llm-provider openai --model gpt-4o-mini "create an nginx deployment with 3 replicas"
```

## Common Errors

If you see:

```text
GEMINI_API_KEY environment variable not set
```

then `kubectl-ai` is still using the default Gemini provider. Pass the correct provider explicitly or export `GEMINI_API_KEY`.

If you see:

```text
OpenAI streaming error ... 429 Too Many Requests ... insufficient_quota
```

then the OpenAI provider is configured correctly, but the API account does not currently have usable quota or billing for the request.

In that case, use one of these options:

- fix billing/quota for the OpenAI account
- switch to Gemini with `GEMINI_API_KEY`
- use the local Ollama path in `01-local-ollama-foundation.md`

## What Just Happened?

You used AI as a Kubernetes copilot. It can speed up drafting, explanation, and discovery, but it still depends on the user to verify output and supply the right context.

In the next exercise, you will build a read-only MCP server so AI tooling can inspect real cluster state instead of relying only on prompts.
