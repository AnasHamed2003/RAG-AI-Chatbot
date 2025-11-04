#!/bin/bash
echo "🔍 Checking llama3:8b model status on server"
echo "=========================================="

# Check if Ollama is running
echo -e "\n1. Checking if Ollama service is running..."
if pgrep -f "ollama serve" > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running"
    echo "   Start it with: ollama serve"
    exit 1
fi

# Check available models
echo -e "\n2. Checking available models..."
ollama list

# Verify llama3:8b is available
echo -e "\n3. Verifying llama3:8b model..."
if ollama list | grep -q "llama3:8b"; then
    echo "✅ llama3:8b model is available"
else
    echo "❌ llama3:8b model not found"
    echo "   Pull it with: ollama pull llama3:8b"
    exit 1
fi

# Test basic model response
echo -e "\n4. Testing basic model response..."
echo "Testing llama3:8b with a simple prompt..."
RESPONSE=$(ollama run llama3:8b "Say 'Hello from llama3:8b!' and nothing else." 2>/dev/null | head -1)
if [[ "$RESPONSE" == *"Hello from llama3:8b!"* ]]; then
    echo "✅ llama3:8b responds correctly"
else
    echo "⚠️  Unexpected response: $RESPONSE"
fi

# Check chatbot container status
echo -e "\n5. Checking chatbot container..."
if command -v docker &> /dev/null; then
    if docker ps | grep -q chatbot; then
        echo "✅ Chatbot container is running"
        echo "   Container logs:"
        docker logs chatbot-chatbot-1 2>&1 | tail -5
    else
        echo "❌ Chatbot container not running"
        echo "   Check with: docker ps -a"
    fi
else
    echo "⚠️  Docker not found, checking if chatbot is running directly..."
    if pgrep -f "python main.py" > /dev/null; then
        echo "✅ Chatbot appears to be running (direct Python)"
    else
        echo "❌ Chatbot not found running"
    fi
fi

# Test API endpoint
echo -e "\n6. Testing chatbot API..."
if command -v curl &> /dev/null; then
    RESPONSE=$(curl -s -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"question": "What model are you using?", "conversation_id": "model_test"}' 2>/dev/null)

    if [[ "$RESPONSE" == *"answer"* ]]; then
        echo "✅ API is responding"
        echo "   Response preview: ${RESPONSE:0:100}..."
    else
        echo "❌ API not responding or returned error"
        echo "   Response: $RESPONSE"
    fi
else
    echo "⚠️  curl not available, cannot test API"
fi

echo -e "\n7. Next steps:"
echo "   - If all checks pass: Your llama3:8b model is working!"
echo "   - Run the test script: python3 test_chatbot_server_fixed.py"
echo "   - Check Docker logs: docker logs chatbot-chatbot-1"
echo "   - Monitor performance: The 8B model may be slower than 3.2B"

echo -e "\n=========================================="
echo "🎉 Model verification complete!"