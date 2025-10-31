# Data Model

## Entities

### ChatRequest
- **question**: string - The user's question to be answered by the chatbot

### ChatResponse
- **answer**: string - The generated answer from the RAG system

## Relationships
- ChatRequest produces ChatResponse through the RAG chain

## Validation Rules
- question: Required, non-empty string, max length 1000 characters
- answer: Generated string, may contain markdown formatting

## State Transitions
- Request received → Context retrieved → Answer generated → Response sent