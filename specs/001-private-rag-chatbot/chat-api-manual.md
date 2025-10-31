# Chat API Manual

## Overview

The Chat API provides a conversational interface for querying your private document knowledge base using Retrieval-Augmented Generation (RAG). It accepts natural language questions and returns answers based solely on the content of uploaded documents.

## Endpoint

**URL**: `POST /chat`  
**Base URL**: `http://localhost:8000` (development)  
**Content-Type**: `application/json`

## Request Format

### Request Body

The request must be sent as JSON with the following structure:

```json
{
  "question": "string"
}
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | The natural language question to ask about your documents. Should be clear and specific for best results. |

### Example Request

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What are the main features of our product?"
     }'
```

Or using PowerShell:

```powershell
Invoke-WebRequest -Uri "http://localhost:8000/chat" `
                 -Method POST `
                 -ContentType "application/json" `
                 -Body '{"question": "What are the main features of our product?"}'
```

## Response Format

### Success Response (200 OK)

```json
{
  "answer": "string"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | The AI-generated answer based on your uploaded documents. The response is limited to information found in the knowledge base. |

### Example Success Response

```json
{
  "answer": "Based on the uploaded documentation, our product includes the following main features: 1) Advanced search capabilities, 2) Real-time collaboration tools, 3) Integration with popular cloud services, and 4) Comprehensive security measures."
}
```

## Error Responses

### 422 Unprocessable Entity (Validation Error)

Returned when the request body is malformed or missing required fields.

```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error

Returned when there's an issue with the RAG pipeline or backend services.

```json
{
  "detail": "Internal server error"
}
```

## Usage Guidelines

### Best Practices

1. **Be Specific**: Ask clear, specific questions rather than vague ones
2. **Context Matters**: The AI can only answer based on uploaded documents
3. **Document Coverage**: Ensure relevant documents are uploaded before asking questions
4. **Question Length**: Keep questions concise but descriptive

### Rate Limiting

Currently, there are no rate limits implemented. However, each request involves AI processing, so avoid excessive concurrent requests.

### Authentication

No authentication is required for the current implementation.

## Testing the API

### Using curl

```bash
# Test with a simple question
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is machine learning?"}'

# Test with a more complex question
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "How does our system handle user authentication?"}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/chat"
data = {"question": "What are the system requirements?"}

response = requests.post(url, json=data)
if response.status_code == 200:
    print("Answer:", response.json()["answer"])
else:
    print("Error:", response.status_code, response.text)
```

### Using JavaScript (Browser)

```javascript
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What is the main purpose of this application?'
  })
})
.then(response => response.json())
.then(data => console.log('Answer:', data.answer))
.catch(error => console.error('Error:', error));
```

## Troubleshooting

### Common Issues

1. **"No relevant documents found"**: Upload documents containing information related to your question
2. **Empty or irrelevant answers**: Try rephrasing your question or check document content
3. **Connection errors**: Ensure the backend server is running on port 8000
4. **CORS errors**: If accessing from a web browser, ensure CORS is properly configured

### Debug Steps

1. Verify the backend is running: `curl http://localhost:8000/`
2. Check uploaded documents: `curl http://localhost:8000/documents`
3. Test with simple questions first
4. Check server logs for detailed error information

## Integration Examples

### React Component

```jsx
import React, { useState } from 'react';

function ChatComponent() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setAnswer(data.answer);
      } else {
        setAnswer('Error: ' + response.statusText);
      }
    } catch (error) {
      setAnswer('Error: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={askQuestion} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      <div>Answer: {answer}</div>
    </div>
  );
}

export default ChatComponent;
```

### Python Client

```python
import requests

class ChatClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def ask(self, question):
        """Ask a question and get an answer."""
        url = f"{self.base_url}/chat"
        response = requests.post(url, json={"question": question})
        response.raise_for_status()
        return response.json()["answer"]

# Usage
client = ChatClient()
answer = client.ask("What are the key benefits?")
print(answer)
```

## API Version

**Version**: 1.0  
**Last Updated**: October 30, 2025  
**Compatible With**: Backend v1.0 with Ollama and ChromaDB integration