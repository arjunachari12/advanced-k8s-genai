import kopf
from graph import graph

@kopf.on.create('aiops.example.com', 'v1', 'rcarequests')
def create_fn(spec, status, namespace, patch, **kwargs):
    pod = spec.get("podName")
    ns = spec.get("namespace", namespace)

    result = graph.invoke({
        "namespace": ns,
        "pod_name": pod,
        "plan": "",
        "pod_report": "",
        "events": "",
        "logs": "",
        "analysis": "",
        "fix": ""
    })

    patch.status["phase"] = "Completed"
    patch.status["plan"] = result["plan"]
    patch.status["analysis"] = result["analysis"]
    patch.status["fix"] = result["fix"]

    return None
