# Exercise 1: Install Prerequisites

This exercise prepares your local environment for Operator SDK development on macOS, Linux, or Windows WSL.

## What You Need

- Docker with Kubernetes-compatible container support
- `kubectl`
- `kind`
- `make`
- `git`
- an existing KIND cluster named `multi-node-cluster`

Verify the basics:

```bash
docker version
kubectl version --client
kind version
make --version
git --version
```

## Install Go

The lab was tested with Go `1.26.1`.

### macOS

```bash
brew install go
go version
```

### Linux or Windows WSL

```bash
mkdir -p /home/$USER/.local/lib
cd /tmp

curl -LO https://go.dev/dl/go1.26.1.linux-amd64.tar.gz
rm -rf /home/$USER/.local/lib/go-toolchain
mkdir -p /home/$USER/.local/lib/go-toolchain
tar -C /home/$USER/.local/lib/go-toolchain --strip-components=1 -xzf go1.26.1.linux-amd64.tar.gz
```

Add Go to your shell:

```bash
echo 'export PATH="$HOME/.local/lib/go-toolchain/go/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
go version
```

## Install Operator SDK

The lab was tested with Operator SDK `v1.42.2`.

### macOS

```bash
brew install operator-sdk
operator-sdk version
```

### Linux or Windows WSL

```bash
mkdir -p /home/$USER/.local/bin
curl -Lo /home/$USER/.local/bin/operator-sdk \
  https://github.com/operator-framework/operator-sdk/releases/download/v1.42.2/operator-sdk_linux_amd64
chmod +x /home/$USER/.local/bin/operator-sdk
```

Add it to your shell if needed:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
operator-sdk version
```

## Verify Cluster Access

```bash
kubectl config current-context
kubectl get nodes -o wide
```

Expected context:

```text
kind-multi-node-cluster
```

## What Just Happened?

You installed the Go and Operator SDK toolchain that powers the rest of the module and verified that your local cluster is reachable before you start building the operator.
