
from tools.k8s_logs import get_logs, get_pod_report, get_recent_events

def run(state):
    pod_report = get_pod_report(state["namespace"], state["pod_name"])
    events = get_recent_events(state["namespace"], state["pod_name"])
    logs = get_logs(state["namespace"], state["pod_name"])
    return {**state, "pod_report": pod_report, "events": events, "logs": logs}
