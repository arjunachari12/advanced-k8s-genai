"""FastAPI application for generating product marketing copy with a local LLM."""

import logging
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator


APP_NAME = os.getenv("APP_NAME", "genai-api")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LLM_URL = os.getenv("LLM_URL", "http://llm:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(APP_NAME)


class GenerateRequest(BaseModel):
    """Incoming request model for the workshop UI."""

    product: str = Field(..., min_length=2, max_length=200)
    audience: str = Field(..., min_length=2, max_length=200)


class GenerateResponse(BaseModel):
    """API response model that is easy for beginners to inspect."""

    model: str
    prompt: str
    content: str


def build_prompt(product: str, audience: str) -> str:
    """Create a clear, structured prompt for consistent model outputs."""

    return f"""
You are a helpful product marketing assistant.

Task:
Write a concise product message for the input below.

Product:
{product}

Target audience:
{audience}

Output requirements:
- Write a short headline.
- Follow with 3 short bullet points.
- Keep the tone practical and clear.
- Avoid hype and unsupported claims.
""".strip()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create and clean up the shared HTTP client."""

    logger.info("Starting %s with model=%s and llm_url=%s", APP_NAME, MODEL_NAME, LLM_URL)
    app.state.http_client = httpx.AsyncClient(timeout=OLLAMA_TIMEOUT_SECONDS)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title=APP_NAME, version="1.0.0", lifespan=lifespan)

# Expose default HTTP metrics on /metrics for Prometheus scraping.
Instrumentator(excluded_handlers=["/health"]).instrument(app).expose(app)


@app.get("/health")
async def health() -> JSONResponse:
    """Health endpoint used by Kubernetes probes and workshop validation."""

    try:
        response = await app.state.http_client.get(f"{LLM_URL}/api/tags")
        response.raise_for_status()
        llm_status = "up"
    except Exception as exc:  # pragma: no cover - defensive operational path
        logger.warning("Health check could not reach Ollama: %s", exc)
        llm_status = "degraded"

    return JSONResponse(
        content={
            "status": "ok",
            "service": APP_NAME,
            "model": MODEL_NAME,
            "llm_status": llm_status,
        }
    )


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate text by forwarding a structured prompt to Ollama."""

    prompt = build_prompt(request.product.strip(), request.audience.strip())
    logger.info("Received generation request for product=%s audience=%s", request.product, request.audience)

    try:
        response = await app.state.http_client.post(
            f"{LLM_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.TimeoutException as exc:
        logger.exception("Timed out while calling Ollama")
        raise HTTPException(status_code=504, detail="The request to the local LLM timed out.") from exc
    except httpx.HTTPStatusError as exc:
        logger.exception("Ollama returned an HTTP error")
        raise HTTPException(status_code=502, detail=f"Ollama returned an error: {exc.response.text}") from exc
    except httpx.HTTPError as exc:
        logger.exception("Failed to reach Ollama")
        raise HTTPException(status_code=503, detail="The API could not reach the local LLM service.") from exc

    content = payload.get("response", "").strip()
    if not content:
        logger.error("Ollama returned an empty response payload: %s", payload)
        raise HTTPException(status_code=502, detail="The local LLM returned an empty response.")

    return GenerateResponse(model=MODEL_NAME, prompt=prompt, content=content)
