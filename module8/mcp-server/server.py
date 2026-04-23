import json
import sys

from fastmcp import FastMCP
from kubernetes import client, config


mcp = FastMCP("Kubernetes Read-Only MCP Server")


def load_kube_config() -> None:
    try:
        config.load_incluster_config()
        print("Loaded in-cluster Kubernetes config.", file=sys.stderr)
    except config.ConfigException:
        config.load_kube_config()
        print("Loaded local kubeconfig.", file=sys.stderr)


load_kube_config()
core_v1 = client.CoreV1Api()


def json_text(payload: object) -> str:
    return json.dumps(payload, indent=2)


@mcp.tool()
def get_cluster_nodes() -> str:
    """Return node names and readiness information for the cluster."""
    nodes = core_v1.list_node().items
    payload = []
    for node in nodes:
        ready_condition = next(
            (condition for condition in node.status.conditions if condition.type == "Ready"),
            None,
        )
        payload.append(
            {
                "name": node.metadata.name,
                "ready": ready_condition.status if ready_condition else "Unknown",
                "kubelet_version": node.status.node_info.kubelet_version,
            }
        )
    return json_text(payload)


@mcp.tool()
def get_namespaces() -> str:
    """Return all namespace names in the cluster."""
    namespaces = core_v1.list_namespace().items
    return json_text([item.metadata.name for item in namespaces])


@mcp.tool()
def get_pods_in_namespace(namespace: str = "default") -> str:
    """Return pod status details for a namespace."""
    pods = core_v1.list_namespaced_pod(namespace=namespace).items
    payload = []
    for pod in pods:
        payload.append(
            {
                "name": pod.metadata.name,
                "phase": pod.status.phase,
                "pod_ip": pod.status.pod_ip,
                "node": pod.spec.node_name,
                "containers": [
                    {
                        "name": container.name,
                        "image": container.image,
                    }
                    for container in pod.spec.containers
                ],
                "container_statuses": [
                    {
                        "name": status.name,
                        "ready": status.ready,
                        "restart_count": status.restart_count,
                        "state": (
                            "waiting"
                            if status.state.waiting
                            else "running"
                            if status.state.running
                            else "terminated"
                            if status.state.terminated
                            else "unknown"
                        ),
                        "reason": (
                            status.state.waiting.reason
                            if status.state.waiting
                            else status.state.terminated.reason
                            if status.state.terminated
                            else ""
                        ),
                    }
                    for status in (pod.status.container_statuses or [])
                ],
            }
        )
    return json_text(payload)


@mcp.tool()
def get_pod_logs(namespace: str, pod_name: str, tail_lines: int = 50, container: str = "") -> str:
    """Return recent logs for a pod container."""
    logs = core_v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace,
        container=container or None,
        tail_lines=tail_lines,
        timestamps=True,
    )
    return logs or "No log lines returned."


@mcp.tool()
def get_recent_events(namespace: str = "default", limit: int = 20) -> str:
    """Return the most recent warning and normal events for a namespace."""
    events = core_v1.list_namespaced_event(namespace=namespace).items
    sorted_events = sorted(
        events,
        key=lambda item: (
            item.last_timestamp
            or item.event_time
            or item.metadata.creation_timestamp
        ),
        reverse=True,
    )
    payload = []
    for event in sorted_events[:limit]:
        payload.append(
            {
                "type": event.type,
                "reason": event.reason,
                "object": f"{event.involved_object.kind}/{event.involved_object.name}",
                "message": event.message,
                "time": str(
                    event.last_timestamp
                    or event.event_time
                    or event.metadata.creation_timestamp
                ),
            }
        )
    return json_text(payload)


if __name__ == "__main__":
    print("Starting K8s MCP Server on 0.0.0.0:8000...", file=sys.stderr)
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
