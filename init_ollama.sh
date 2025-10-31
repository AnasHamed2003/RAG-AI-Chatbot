#!/bin/bash

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 2
done

echo "Ollama is ready. Pulling models..."

# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text

echo "Models pulled successfully!"