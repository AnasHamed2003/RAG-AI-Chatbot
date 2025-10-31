# Quickstart Guide

## Prerequisites

- Python 3.11
- Ollama installed and running with models `llama3` and `nomic-embed-text`
- ChromaDB vector store at `./chroma_db`

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

3. Verify models are available:
   ```bash
   ollama list
   ```
   Should show `llama3` and `nomic-embed-text`

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

1. Health check:
   ```bash
   curl http://localhost:8000/
   ```

2. Chat endpoint:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "What is in my documents?"}'
   ```

## API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI.