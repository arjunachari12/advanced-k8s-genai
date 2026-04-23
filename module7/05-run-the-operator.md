# Exercise 5: Run the Operator Locally

In this exercise, the controller runs on your laptop while managing resources in the KIND cluster.

## Create the Lab Namespace

```bash
kubectl create namespace ai-operators-lab --dry-run=client -o yaml | kubectl apply -f -
```

## Start the Controller

Use one terminal window for the operator:

```bash
cd module7
export PATH="/home/arjun/.local/bin:/home/arjun/.local/lib/go-toolchain/go/bin:$PATH"

make run
```

If you have not validated the project yet, run `make test` once before `make run`.

When the controller starts successfully, you should see log lines similar to:

```text
INFO  setup  starting manager
INFO  Starting Controller  {"controller": "aiapp"}
INFO  Starting workers     {"controller": "aiapp", "worker count": 1}
```

Keep that terminal open.

## Open a Second Terminal

All remaining commands in the module can run from another shell session while `make run` continues in the first one.

## What Just Happened?

The operator is now connected to the Kubernetes API and watching `AIApp` resources. Nothing is reconciled yet because no custom resource exists.
