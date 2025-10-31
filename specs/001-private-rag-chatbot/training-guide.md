# Training and Knowledge Expansion Guide

## Overview

Your RAG chatbot can be "trained" and expanded in several ways. Since this is a Retrieval-Augmented Generation system, training involves expanding the knowledge base rather than fine-tuning the language model. Here are all the methods available:

## 1. Document Upload (Existing)

**Endpoint**: `POST /upload`
**Purpose**: Add documents to the knowledge base

### Supported File Types
- **Documents**: PDF, DOCX, TXT
- **Spreadsheets**: XLSX, XLS, CSV
- **Presentations**: PPTX
- **Images**: PNG, JPG, JPEG, BMP, TIFF (with OCR)

### Example
```bash
curl -X POST "http://localhost:8000/upload" \
     -F "file=@document.pdf"
```

## 2. Direct Text Input (Existing)

**Endpoint**: `POST /upload-text`
**Purpose**: Add text content directly

### Example
```json
{
  "text": "Your custom knowledge or information here..."
}
```

## 3. Conversational Learning (NEW)

**Endpoint**: `POST /add-knowledge`
**Purpose**: Add information learned during conversations

### Request Format
```json
{
  "text": "The specific information to add",
  "source": "conversation_2025_10_30",
  "category": "user_correction"
}
```

### Use Cases
- User corrections: "Actually, the answer should be..."
- New facts learned during conversation
- Important context from user interactions

## 4. User Feedback System (NEW)

**Endpoint**: `POST /feedback`
**Purpose**: Collect feedback to identify knowledge gaps

### Request Format
```json
{
  "conversation_id": "conv_123",
  "question": "What is the capital of France?",
  "answer": "Paris",
  "rating": 5,
  "feedback": "Correct answer"
}
```

### Benefits
- Track response quality
- Identify frequently asked questions
- Discover missing knowledge areas

## 5. Conversational Memory (NEW)

**Feature**: Each conversation now maintains context
**Benefit**: Follow-up questions can reference previous context

### Usage
```json
{
  "question": "What did we discuss earlier?",
  "conversation_id": "my_conversation_1"
}
```

## API Endpoints Summary

### Knowledge Addition
- `POST /upload` - Upload files
- `POST /upload-text` - Add text directly
- `POST /add-knowledge` - Add learned information

### Conversation Management
- `POST /chat` - Chat with memory (include `conversation_id`)
- `GET /conversations` - List active conversations
- `DELETE /conversation/{id}` - Clear conversation memory

### Feedback & Analytics
- `POST /feedback` - Submit response feedback
- `GET /feedback` - View recent feedback

## Training Strategies

### 1. Bulk Document Upload
```bash
# Upload multiple documents
for file in *.pdf; do
  curl -X POST "http://localhost:8000/upload" -F "file=@$file"
done
```

### 2. Continuous Learning Loop
1. User asks question
2. If answer is incomplete/incorrect, user provides correction
3. System adds correction via `/add-knowledge`
4. Future similar questions get better answers

### 3. Feedback-Driven Improvement
1. Collect feedback on responses
2. Analyze patterns in low-rated answers
3. Add missing information to knowledge base
4. Retrain on improved dataset

### 4. Domain-Specific Training
```bash
# Add domain-specific knowledge
curl -X POST "http://localhost:8000/add-knowledge" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Company policy: Remote work is available for all employees",
    "source": "hr_policy_update",
    "category": "company_policies"
  }'
```

## Best Practices

### Content Quality
- Use clear, well-structured documents
- Include relevant metadata in filenames
- Break large documents into logical sections
- Use consistent terminology

### Conversation Management
- Use meaningful conversation IDs for different topics
- Clear memory when switching contexts
- Encourage users to provide feedback

### Knowledge Organization
- Categorize information when adding via `/add-knowledge`
- Use descriptive source names
- Regularly review and update knowledge base

## Monitoring & Maintenance

### Check Knowledge Base
```bash
# List all documents
curl http://localhost:8000/documents

# View recent feedback
curl http://localhost:8000/feedback
```

### Performance Monitoring
- Track response quality through feedback
- Monitor conversation lengths
- Identify frequently asked questions

### Knowledge Base Maintenance
- Regularly review and update documents
- Remove outdated information
- Backup knowledge base periodically

## Advanced Training Techniques

### 1. Iterative Refinement
1. Deploy system with initial knowledge
2. Collect user interactions and feedback
3. Identify knowledge gaps
4. Add missing information
5. Repeat cycle

### 2. User-Generated Content
- Allow power users to contribute knowledge
- Implement approval workflow for contributions
- Use voting system for content quality

### 3. Automated Learning
- Analyze conversation patterns
- Automatically suggest knowledge additions
- Implement confidence scoring for responses

## Implementation Example

Here's how to implement a learning loop in your application:

```javascript
// After getting a response, ask for feedback
async function submitFeedback(conversationId, question, answer, rating, feedback) {
  await fetch('/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      conversation_id: conversationId,
      question,
      answer,
      rating,
      feedback
    })
  });
}

// Allow users to add corrections
async function addUserCorrection(text, source) {
  await fetch('/add-knowledge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      source: source || 'user_correction',
      category: 'correction'
    })
  });
}
```

## Conclusion

Your RAG system now supports multiple ways to "train" and improve:

1. **Static Knowledge**: Upload documents and text
2. **Dynamic Learning**: Add information from conversations
3. **User Feedback**: Collect and analyze response quality
4. **Conversational Memory**: Maintain context across interactions

This creates a continuously improving system that learns from user interactions while maintaining the benefits of retrieval-augmented generation.