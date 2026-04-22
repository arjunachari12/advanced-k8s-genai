#!/usr/bin/env bash
set -euo pipefail

echo "Checking local workshop toolchain"

check_cmd() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    echo "[ok] $name: $(command -v "$name")"
  else
    echo "[missing] $name"
  fi
}

check_cmd docker
check_cmd kubectl
check_cmd kind
check_cmd helm
check_cmd git
check_cmd make
check_cmd python3

echo
echo "Checking Kubernetes context"

if kubectl config current-context >/dev/null 2>&1; then
  context="$(kubectl config current-context)"
  echo "[ok] current context: $context"
else
  echo "[warn] no current kubectl context"
  exit 0
fi

if kubectl cluster-info >/dev/null 2>&1; then
  echo "[ok] Kubernetes API is reachable"
else
  echo "[warn] Kubernetes API is not reachable from the current context"
  echo "[hint] recreate the cluster with: cd module1 && kind create cluster --name multi-node-cluster --config kind-config.yaml"
fi
