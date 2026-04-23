
import os

from langchain_ollama import ChatOllama


OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_BASE_URL",
    "http://ollama.genai.svc.cluster.local:11434",
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")

def run(state):
    prompt = f"Plan a beginner-friendly debugging sequence for pod {state['pod_name']} in namespace {state['namespace']}."
    try:
        llm = ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
        return {**state, "plan": llm.invoke(prompt).content}
    except Exception:
        return {
            **state,
            "plan": "1. Inspect pod status 2. Inspect recent pod events 3. Inspect logs if the container started 4. Suggest the smallest safe fix.",
        }
