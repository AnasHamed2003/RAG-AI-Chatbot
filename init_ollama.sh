#!/bin/bash

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
sleep 10

echo "Ollama should be ready now. Pulling models..."

# Pull required models
ollama pull llama3:8b
ollama pull nomic-embed-text

echo "Models pulled successfully! Ollama is running."

# Wait for the Ollama process
wait $OLLAMA_PID