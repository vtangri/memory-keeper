FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (e.g., for audio processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (FastAPI default)
EXPOSE 8000

# Download spacy model during build to cache it
RUN python -m spacy download en_core_web_sm

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
