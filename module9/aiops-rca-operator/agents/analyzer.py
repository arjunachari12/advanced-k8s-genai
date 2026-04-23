
import json

def run(state):
    pod_report = json.loads(state["pod_report"])
    events = state.get("events", "")
    logs = state["logs"]
    statuses = pod_report.get("container_statuses") or []

    for status in statuses:
        waiting_reason = status.get("waiting_reason", "")
        if waiting_reason in {"ImagePullBackOff", "ErrImagePull", "InvalidImageName"}:
            return {**state, "analysis": waiting_reason}
        if waiting_reason == "CrashLoopBackOff":
            return {**state, "analysis": "CrashLoopBackOff"}

    if "OOMKilled" in logs:
        return {**state, "analysis": "OOMKilled"}
    if "CrashLoopBackOff" in logs:
        return {**state, "analysis": "CrashLoopBackOff"}
    if "ImagePullBackOff" in events or "ErrImagePull" in events:
        return {**state, "analysis": "ImagePullBackOff"}
    return {**state, "analysis": "Unknown"}
