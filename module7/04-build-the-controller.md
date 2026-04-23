# Exercise 4: Build the Controller

This controller watches `AIApp` resources and reconciles a Deployment and Service for each one.

## Review the Reconciler

Open:

`internal/controller/aiapp_controller.go`

Key ideas to look for:

- `Reconcile()` fetches the `AIApp`
- `CreateOrUpdate()` keeps a `Deployment` in sync
- `CreateOrUpdate()` keeps a `Service` in sync
- status conditions explain whether the workload is still converging or ready
- `SetupWithManager()` declares resource ownership and watches

## Build the Project

```bash
cd module7
export PATH="$HOME/.local/bin:$HOME/.local/lib/go-toolchain/go/bin:$PATH"

make build
make test
```

These targets run:

- `make manifests`
- `make generate`
- `go fmt`
- `go vet`
- `go build`
- envtest-backed controller tests

If the first run feels slow, let it finish. Go is usually warming module and type-check caches.

## Why This Controller Is Useful for the Lab

The operator automates a real workload lifecycle:

- creates the application `Deployment`
- exposes it through a `Service`
- passes AI-specific environment variables into the container
- updates `status` so users can see the result without inspecting multiple resources

## What Just Happened?

You compiled an operator that translates a custom Kubernetes object into standard runtime resources. This is the core operator pattern: users describe intent in a custom API, and the controller keeps reality aligned with that intent.
