# Training Repo Readiness Report

## Summary

The repository is organized into `module1` through `module9` and now aligns with the workshop agenda. The major follow-along issues found during the audit were stale paths left over from the earlier restructure, inconsistent README formats, and unclear assumptions about where commands should be run from.

## What Was Broken

- Module documentation still contained older path patterns and stale references.
- Module 6 labs still referenced `training/manifests/...` instead of the current `module6/manifests/...` layout.
- The root README was too thin for instructor use and did not include a dependency map or progression guidance.
- Several module READMEs lacked predictable sections such as troubleshooting, cleanup, and validation checklists.
- There was no simple repo-level environment verification helper.

## What Was Fixed

### Module 1

- Updated the README with learning objectives, architecture, validation checks, troubleshooting, and cleanup.
- Removed the old absolute path reference and aligned commands with the current repo layout.

### Module 2

- Expanded the README with learning objectives, architecture, troubleshooting, cleanup, and an instructor checklist.
- Confirmed the API and UI images build successfully.

### Module 3

- Expanded the README with architecture, validation checks, troubleshooting, cleanup, and an instructor checklist.

### Module 4

- Reframed the README around learning objectives, module flow, validation, troubleshooting, cleanup, and instructor checks.

### Module 5

- Expanded the README with chart architecture, troubleshooting, cleanup, and instructor checks.
- Confirmed Helm lint and template rendering work.

### Module 6

- Fixed stale paths in the ArgoCD and rollout labs.
- Expanded the README with architecture, troubleshooting, cleanup, and instructor checks.

### Module 7

- Expanded the README with operator architecture, troubleshooting, cleanup, and instructor checks.
- Kept the Operator SDK project layout intact.

### Module 8

- Expanded the README with architecture, validation checks, troubleshooting, cleanup, and instructor checks.
- Confirmed the MCP server image builds successfully.

### Module 9

- Expanded the README with architecture, troubleshooting, and instructor checks.
- Confirmed the agent image builds successfully.

### Root Repo

- Rewrote `README.md` to include course overview, prerequisites, repo structure, delivery order, dependency map, and setup guidance.
- Added `scripts/verify-env.sh`.

## Validation Performed

These commands were executed successfully:

```bash
make validate
docker build -t module2-api-test:local module2/api
docker build -t module2-ui-test:local module2/ui
docker build -t module8-mcp-test:local module8/mcp-server
docker build -t module9-agent-test:local module9/ai-agent
./scripts/verify-env.sh
```

Static validation also confirmed:

- non-template YAML files parse successfully
- the Helm chart renders successfully through `helm template`
- Compose files in Modules 2 and 8 render successfully through `docker compose config`

## Remaining Manual Verification

The active kube-context is `kind-multi-node-cluster`, but at validation time the Kubernetes API endpoint was not reachable. Because of that, these items still require a live cluster to verify end to end:

- `kubectl apply` and runtime validation for Modules 2 through 9
- live Grafana, Loki, and Prometheus behavior in Module 3
- KEDA scale-up behavior in Module 4
- ArgoCD sync and Argo Rollouts execution in Module 6
- Operator runtime behavior in Module 7
- in-cluster MCP and agent flows in Modules 8 and 9

## Environment Limitations

- `go` was not installed in the validation shell, so Module 7 Go builds and tests could not be executed here.
- The Kubernetes API for the current context was unreachable, so live cluster checks were not possible in this environment.

## Instructor Next Steps

Before class:

1. Recreate the KIND cluster if `kubectl cluster-info` fails.
2. Run `make validate`.
3. Run `./scripts/verify-env.sh`.
4. Walk through the module READMEs in order and validate live cluster steps where needed.
