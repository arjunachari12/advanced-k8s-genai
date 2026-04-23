# Exercise 8: Cleanup

Use this exercise after you finish the module.

If `make run` is still active in another terminal, stop it first with `Ctrl+C`.

## Delete the Sample Custom Resources

```bash
cd module7
kubectl delete -f config/samples/ai_v1alpha1_aiapp.yaml --ignore-not-found
kubectl delete -f config/samples/ai_v1alpha1_aiapp_minimal.yaml --ignore-not-found
```

## Uninstall the CRD

```bash
export PATH="$HOME/.local/bin:$HOME/.local/lib/go-toolchain/go/bin:$PATH"
make uninstall
```

## Delete the Lab Namespace

```bash
kubectl delete namespace ai-operators-lab --ignore-not-found
```

## What Just Happened?

Cleanup removes both the custom resources and the API extension itself. Once the CRD is uninstalled, Kubernetes no longer recognizes `AIApp` objects.
