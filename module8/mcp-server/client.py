import asyncio
import json
from typing import Any

from fastmcp import Client


def load_json(result: Any) -> Any:
    if getattr(result, "data", None):
        return json.loads(result.data)
    text = result.content[0].text if getattr(result, "content", None) else "[]"
    return json.loads(text)


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def print_nodes(nodes: list[dict[str, Any]]) -> None:
    for node in nodes:
        print(
            f"- {node['name']}: Ready={node['ready']}, "
            f"Kubelet={node['kubelet_version']}"
        )


def summarize_pod(pod: dict[str, Any]) -> str:
    statuses = pod.get("container_statuses", [])
    if statuses:
        reasons = [
            status.get("reason")
            for status in statuses
            if status.get("reason")
        ]
        if reasons:
            return ", ".join(reasons)
    return pod.get("phase", "Unknown")


def print_pods(namespace: str, pods: list[dict[str, Any]]) -> None:
    if not pods:
        print(f"No pods found in namespace '{namespace}'.")
        return

    for pod in pods:
        images = ", ".join(
            container["image"] for container in pod.get("containers", [])
        )
        print(
            f"- {pod['name']}: phase={pod['phase']}, "
            f"node={pod['node']}, image={images}, status={summarize_pod(pod)}"
        )


def find_unhealthy_pods(pods: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unhealthy = []
    for pod in pods:
        if pod.get("phase") != "Running":
            unhealthy.append(pod)
            continue
        for status in pod.get("container_statuses", []):
            if not status.get("ready", False) or status.get("reason"):
                unhealthy.append(pod)
                break
    return unhealthy


def print_events(events: list[dict[str, Any]], pod_name: str) -> None:
    matching_events = [
        event for event in events if pod_name in event.get("object", "")
    ]
    if not matching_events:
        print(f"No recent events found for pod '{pod_name}'.")
        return

    for event in matching_events[:5]:
        print(
            f"- [{event['type']}] {event['reason']} on {event['object']}: "
            f"{event['message']}"
        )


async def main() -> None:
    client = Client("http://localhost:8000/sse")

    async with client:
        print("Connected to FastMCP server.")

        tools = await client.list_tools()
        print_section("Available Tools")
        print(", ".join(tool.name for tool in tools))

        print_section("Cluster Nodes")
        nodes = load_json(await client.call_tool("get_cluster_nodes"))
        print_nodes(nodes)

        print_section("Pods In default")
        default_pods = load_json(
            await client.call_tool("get_pods_in_namespace", {"namespace": "default"})
        )
        print_pods("default", default_pods)

        print_section("Pods In genai")
        genai_pods = load_json(
            await client.call_tool("get_pods_in_namespace", {"namespace": "genai"})
        )
        print_pods("genai", genai_pods)

        unhealthy_pods = find_unhealthy_pods(genai_pods)
        print_section("Troubleshooting Summary")
        if not unhealthy_pods:
            print("No unhealthy pods detected in namespace 'genai'.")
            return

        print("Unhealthy pods detected:")
        for pod in unhealthy_pods:
            print(f"- {pod['name']}: {summarize_pod(pod)}")

        events = load_json(
            await client.call_tool("get_recent_events", {"namespace": "genai", "limit": 20})
        )
        target_pod = unhealthy_pods[0]["name"]
        print(f"\nRecent events for {target_pod}:")
        print_events(events, target_pod)


if __name__ == "__main__":
    asyncio.run(main())
