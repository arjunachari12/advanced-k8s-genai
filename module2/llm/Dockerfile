# The official Ollama image provides the runtime for local LLM inference.
FROM ollama/ollama:0.11.10

WORKDIR /app

# curl is used by the startup script to wait until the Ollama API is available.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the startup script into the image.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_MODEL=tinyllama
ENV OLLAMA_HOST=0.0.0.0:11434

EXPOSE 11434

CMD ["/entrypoint.sh"]
