
from typing import TypedDict

class RCAState(TypedDict):
    namespace: str
    pod_name: str
    plan: str
    pod_report: str
    events: str
    logs: str
    analysis: str
    fix: str
