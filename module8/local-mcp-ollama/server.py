import json
import os

import requests
from flask import Flask, Response, request

app = Flask(__name__)

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_DEFAULT_MODEL = os.environ.get("OLLAMA_DEFAULT_MODEL", "tinyllama")


def normalized_ollama_host(raw_host: str) -> str:
    host = raw_host.strip()
    if not host.startswith(("http://", "https://")):
        if ":" not in host:
            host = f"{host}:11434"
        host = f"http://{host}"
    return host.rstrip("/")

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.get_json()
    model = data.get("model", OLLAMA_DEFAULT_MODEL)
    messages = data.get("messages", [])

    # The actual prompt content is in the last message
    prompt_text = ""
    if messages:
        prompt_text = messages[-1].get("content", "")

    # Ollama API payload
    ollama_payload = {
        "model": model,
        "prompt": prompt_text,
        "stream": True
    }

    # Forward the request to Ollama and stream the response
    def generate():
        response = requests.post(
            f"{normalized_ollama_host(OLLAMA_HOST)}/api/generate",
            json=ollama_payload,
            stream=True,
        )
        response.raise_for_status()
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                # We need to format the response to mimic OpenAI's streaming format
                # Ollama's response chunk is a JSON object per line
                ollama_response = json.loads(chunk)
                content = ollama_response.get("response", "")
                
                # Create an OpenAI-compatible streaming chunk
                openai_chunk = {
                    "choices": [{
                        "delta": {
                            "content": content
                        }
                    }]
                }
                yield f"data: {json.dumps(openai_chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
