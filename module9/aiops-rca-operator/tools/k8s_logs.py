
import json

from kubernetes import client, config
from kubernetes.client import exceptions as k8s_exceptions


def load_config():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()


def get_core_v1():
    load_config()
    return client.CoreV1Api()

def get_logs(namespace, pod):
    v1 = get_core_v1()
    try:
        return v1.read_namespaced_pod_log(name=pod, namespace=namespace, tail_lines=100)
    except k8s_exceptions.ApiException as exc:
        return f"Unable to read logs for pod {pod} in namespace {namespace}: {exc.reason}"


def get_pod_report(namespace, pod):
    v1 = get_core_v1()
    try:
        pod_obj = v1.read_namespaced_pod(name=pod, namespace=namespace)
    except k8s_exceptions.ApiException as exc:
        return json.dumps(
            {
                "name": pod,
                "namespace": namespace,
                "error": f"Unable to read pod: {exc.reason}",
            },
            indent=2,
        )

    payload = {
        "name": pod_obj.metadata.name,
        "namespace": pod_obj.metadata.namespace,
        "phase": pod_obj.status.phase,
        "container_statuses": [
            {
                "name": status.name,
                "ready": status.ready,
                "restart_count": status.restart_count,
                "waiting_reason": status.state.waiting.reason if status.state.waiting else "",
                "terminated_reason": status.state.terminated.reason if status.state.terminated else "",
            }
            for status in (pod_obj.status.container_statuses or [])
        ],
    }
    return json.dumps(payload, indent=2)


def get_recent_events(namespace, pod):
    v1 = get_core_v1()
    events = v1.list_namespaced_event(namespace=namespace).items
    pod_events = []
    for event in events:
        if event.involved_object.kind == "Pod" and event.involved_object.name == pod:
            pod_events.append(
                {
                    "type": event.type,
                    "reason": event.reason,
                    "message": event.message,
                    "time": str(
                        event.last_timestamp
                        or event.event_time
                        or event.metadata.creation_timestamp
                    ),
                }
            )
    return json.dumps(pod_events[-10:], indent=2)
