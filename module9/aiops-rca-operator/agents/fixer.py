
import os

from langchain_ollama import ChatOllama


OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_BASE_URL",
    "http://ollama.genai.svc.cluster.local:11434",
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")

def run(state):
    analysis = state["analysis"]
    pod_name = state["pod_name"]
    namespace = state["namespace"]

    deterministic_fixes = {
        "ImagePullBackOff": f"Inspect the image with `kubectl describe pod {pod_name} -n {namespace}` and then correct the image tag or repository in the owning Deployment.",
        "ErrImagePull": f"Inspect the image with `kubectl describe pod {pod_name} -n {namespace}` and then correct the image tag or repository in the owning Deployment.",
        "InvalidImageName": f"Fix the image name in the workload manifest, then reapply it and verify rollout.",
        "CrashLoopBackOff": f"Run `kubectl logs {pod_name} -n {namespace} --previous` and inspect container startup errors, config, command, and environment values.",
        "OOMKilled": f"Check memory limits and application usage. Then adjust requests/limits and redeploy the workload.",
    }
    if analysis in deterministic_fixes:
        return {**state, "fix": deterministic_fixes[analysis]}

    prompt = f"""
Pod report:
{state['pod_report']}

Recent events:
{state['events']}

Logs:
{state['logs']}

Issue:
{analysis}

Suggest a short beginner-friendly Kubernetes fix with one exact next kubectl command.
"""
    try:
        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        return {**state, "fix": llm.invoke(prompt).content}
    except Exception:
        return {
            **state,
            "fix": f"Run `kubectl describe pod {pod_name} -n {namespace}` and inspect recent events before changing the workload.",
        }
