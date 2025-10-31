# Data Model

## Entities

### Question
- **text**: string - The user's query text
- **timestamp**: datetime - When the question was submitted
- **id**: string - Unique identifier

### Answer
- **text**: string - The generated response text
- **timestamp**: datetime - When the answer was generated
- **question_id**: string - Reference to the Question that prompted this answer
- **sources**: array of strings - IDs of document chunks used

### Document Chunk
- **content**: string - The text content of the document chunk
- **metadata**: object - Information about the source document (filename, page, etc.)
- **id**: string - Unique identifier

### Vector Embedding
- **vector**: array of floats - The numerical embedding vector (768 dimensions for nomic-embed-text)
- **chunk_id**: string - Reference to the Document Chunk this embedding represents

## Relationships
- Question 1:N Answer (one question can generate multiple answers, though typically 1:1)
- Document Chunk 1:1 Vector Embedding
- Answer N:N Document Chunk (answer uses multiple chunks as sources)

## Validation Rules
- Question.text: Required, non-empty, max 1000 characters
- Answer.text: Generated content, variable length
- Document Chunk.content: Required, non-empty
- Vector Embedding.vector: Required, exactly 768 float values

## State Transitions
- Question submitted → Relevant chunks retrieved → Answer generated with sources