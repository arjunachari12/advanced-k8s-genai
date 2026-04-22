#!/bin/sh

# This script starts the Ollama API server, waits for it to become reachable,
# and then pulls the selected model so the app is ready for requests.
set -eu

OLLAMA_MODEL="${OLLAMA_MODEL:-tinyllama}"
OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"

export OLLAMA_HOST

echo "Starting Ollama on ${OLLAMA_HOST}"
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to accept HTTP traffic..."
until curl -sf "http://127.0.0.1:11434/api/tags" >/dev/null; do
  sleep 2
done

echo "Pulling model: ${OLLAMA_MODEL}"
ollama pull "${OLLAMA_MODEL}"

echo "Ollama is ready"
wait "${OLLAMA_PID}"
