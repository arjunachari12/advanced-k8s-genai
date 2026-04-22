# Python slim keeps the image small while still being easy to understand in a workshop.
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies first to take advantage of Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the image.
COPY app ./app

EXPOSE 8000

# A single Uvicorn worker is enough for the demo and keeps logs simple for training.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
