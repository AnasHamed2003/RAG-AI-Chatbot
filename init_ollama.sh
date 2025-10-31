#!/bin/bash

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 2
done

echo "Ollama is ready. Pulling models..."

# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text

echo "Models pulled successfully! Ollama is running."

# Wait for the Ollama process
wait $OLLAMA_PID