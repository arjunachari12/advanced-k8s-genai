# Exercise 2: Schedule the Agent with a CronJob

This exercise shows how the same agent can become a recurring operational check.

## What You Are Building

You are turning the one-shot diagnosis Job into a scheduled Kubernetes CronJob.

This is the simplest path from:

- AI-assisted troubleshooting

to

- AI-assisted routine observation

## Why This Matters

Platform teams often need repeated checks, not one-off commands.

A CronJob is useful here because it lets the same agent:

- run on a schedule
- inspect cluster health repeatedly
- produce logs that teams can review

This is also the point where you can discuss future extensions such as:

- Slack notifications
- ticket creation
- approval-based remediation
- policy gates before any write action

## Step 1: Review the CronJob Manifest

Open:

- `module9/ai-agent/k8s/cronjob.yaml`

Notice that it uses the same image and the same core environment variables as the Job version.

The main difference is the schedule:

```text
*/15 * * * *
```

## Step 2: Deploy the CronJob

```bash
kubectl apply -f module9/ai-agent/k8s/cronjob.yaml
kubectl get cronjob -n genai
```

## Step 3: Watch It Create Jobs

```bash
kubectl get jobs -n genai
kubectl get pods -n genai
```

If you do not want to wait for the next scheduled run, you can still keep using the one-shot Job from Exercise 1 for immediate testing.

## Step 4: Inspect the Output

When a CronJob-created Job appears, inspect its logs the same way:

```bash
kubectl logs -n genai job/<job-name>
```

## What Just Happened?

You changed the agent from a manual tool into scheduled automation.

That is an important platform pattern: once an agent is packaged as a Kubernetes workload, standard Kubernetes scheduling and lifecycle features can manage it.

## Cleanup

```bash
kubectl delete cronjob ai-k8s-assistant -n genai --ignore-not-found
```
