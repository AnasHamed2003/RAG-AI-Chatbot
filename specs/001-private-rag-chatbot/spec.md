# Feature Specification: Private RAG Chatbot

**Feature Branch**: `001-private-rag-chatbot`  
**Created**: October 29, 2025  
**Updated**: November 4, 2025  
**Status**: Complete  
**Current Model**: llama3:8b (upgraded from llama3.2)  
**Vector Database**: FAISS (with lazy initialization)  
**Knowledge Base**: SwiftFixPro FAQ (46+ Q&A pairs)  
**Input**: User description: "Goal: Build the FastAPI "Brain" (main.py)

1.  **Task 1: Setup and Connections:**
    * Create the `main.py` file with a basic FastAPI app.
    * Load the required Python libraries (FastAPI, LangChain, Ollama, FAISS).
    * Establish and verify the connections to the two core components:
        * Connect to the *FAISS* vector store with lazy initialization.
        * Connect to the *Ollama* models (`llama3:8b` and `nomic-embed-text`).
    * Create a simple `/` endpoint to confirm the server is running.
    * Implement CORS middleware for cross-origin requests.

2.  **Task 2: Define Data Models:**
    * Use Pydantic (built into FastAPI) to create data models for:
        * `ChatRequest`: A class that expects a `question` string and optional `conversation_id`.
        * `ChatResponse`: A class that will send back an `answer` string and `conversation_id`.
        * `AddKnowledgeRequest`: For adding knowledge directly to the vector database.
        * `FeedbackRequest`: For collecting user feedback on responses.

3.  **Task 3: Build the RAG Chain:**
    * Use LangChain Expression Language (LCEL) to build the full RAG "chain."
    * This chain will define the flow: `input` -> `retriever` -> `prompt` -> `model` -> `output_parser`.
    * This is the core logic that orchestrates the entire RAG process.
    * Implement conversation memory for multi-turn conversations.

4.  **Task 4: Create the Chat Endpoint:**
    * Create a new POST `/chat` endpoint.
    * This endpoint will use the Pydantic models (from Task 2) and the RAG chain (from Task 3).
    * It will receive a question, "invoke" the chain, and return the final answer.
    * Support conversation threading with memory.

5.  **Task 5: Document Upload Functionality:**
    * Create POST `/upload` endpoint to accept file uploads.
    * Support multiple file formats: PDF, TXT, DOCX, PPTX, XLSX, CSV, images.
    * Extract text content from uploaded files using appropriate libraries.
    * Split documents into chunks and store in FAISS vector database.

6.  **Task 6: Document Management:**
    * Create GET `/documents` endpoint to list uploaded documents.
    * Create POST `/upload-text` endpoint for direct text input.
    * Create POST `/add-knowledge` endpoint for programmatic knowledge addition.
    * Track document sources and metadata in vector database.

7.  **Task 7: Knowledge Base Management:**
    * Implement SwiftFixPro FAQ knowledge base with 46+ categorized Q&A pairs.
    * Create automated script for adding structured knowledge.
    * Support different knowledge categories (services, accounts, payments, etc.).

8.  **Task 8: Conversation & Feedback System:**
    * Implement conversation memory for multi-turn interactions.
    * Create feedback collection system for response quality improvement.
    * Add conversation management endpoints (list, clear conversations).

9.  **Task 9: Docker Deployment:**
    * Create Docker setup with Miniconda environment.
    * Implement multi-service deployment (chatbot + Ollama).
    * Add health checks and proper service dependencies.

10. **Task 10: Testing Infrastructure:**
     * Create comprehensive API testing scripts.
     * Implement server-side verification tools.
     * Add model validation and knowledge base testing.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Chat Interaction (Priority: P1)

A user wants to ask questions about their private documents and receive accurate answers based on the document content.

**Why this priority**: This is the core functionality that delivers the primary value of the chatbot - answering questions from private documents.

**Independent Test**: Can be tested by sending a question via API and verifying the response contains relevant information from the documents.

**Acceptance Scenarios**:

1. **Given** the system has ingested private documents, **When** a user sends a question related to the documents, **Then** the system returns an answer based on the document content.
2. **Given** the system is running, **When** a user accesses the health endpoint, **Then** the system confirms it is operational.

---

### User Story 2 - Document Upload (Priority: P1)

A user wants to upload various types of documents (PDF, Word, Excel, etc.) to build their private knowledge base.

**Why this priority**: Without document upload functionality, users cannot populate the knowledge base for the chatbot to answer questions.

**Independent Test**: Can be tested by uploading different file types and verifying they are processed and stored correctly.

**Acceptance Scenarios**:

1. **Given** a user has a PDF file, **When** they upload it via the API, **Then** the system extracts text content and stores it in the vector database.
2. **Given** a user has various file types (DOCX, PPTX, XLSX, CSV, images), **When** they upload them, **Then** the system processes each type appropriately and adds to the knowledge base.
3. **Given** uploaded documents exist, **When** a user requests the document list, **Then** the system returns all uploaded document names.

---

### User Story 3 - Web Interface (Priority: P2)

A user wants a web-based interface to upload documents and chat with their private knowledge base without using API calls directly.

**Why this priority**: Provides a user-friendly way to interact with the system, making it accessible to non-technical users.

**Independent Test**: Can be tested by opening the web interface in a browser and performing upload and chat operations.

**Acceptance Scenarios**:

1. **Given** the web interface is loaded, **When** a user drags and drops files or clicks to select files, **Then** the interface uploads them to the backend and shows success confirmation.
2. **Given** documents are uploaded, **When** a user views the document list, **Then** all uploaded documents are displayed.
3. **Given** documents are uploaded, **When** a user types a question and submits it, **Then** the interface displays the AI-generated answer based on the document content.
4. **Given** the interface is in use, **When** operations are in progress, **Then** appropriate loading indicators are shown.

---

### User Story 4 - Component Connections (Priority: P2)

The system must properly connect to all core components (Ollama, ChromaDB) to function.

**Why this priority**: Without proper connections, the core functionality cannot work.

**Independent Test**: Can be tested by verifying connections to Ollama models and ChromaDB vector store on startup.

**Acceptance Scenarios**:

1. **Given** Ollama is running with required models, **When** the system starts, **Then** it successfully connects to llama3 and nomic-embed-text models.
2. **Given** ChromaDB exists with ingested data, **When** the system starts, **Then** it successfully connects to the vector database.

---

### User Story 5 - Data Model Handling (Priority: P3)

The system must properly handle request and response data structures.

**Why this priority**: Ensures data integrity and proper API communication.

**Independent Test**: Can be tested by validating request/response schemas and data flow.

**Acceptance Scenarios**:

1. **Given** a valid question string, **When** sent to the chat endpoint, **Then** the system processes it using Pydantic models.
2. **Given** the RAG chain generates a response, **When** returned to user, **Then** it follows the ChatResponse structure.

---

### Edge Cases

- What happens when the question has no relevant documents in the vector store?
- How does the system handle very long questions or responses?
- What if Ollama models are not available or fail to load?
- How does the system behave if ChromaDB is empty or corrupted?

## Requirements *(mandatory)*

### Functional Requirements

* **FR-001**: System MUST create a FastAPI application in main.py
* **FR-002**: System MUST load and use FastAPI, LangChain, Ollama, and FAISS libraries
* **FR-003**: System MUST connect to FAISS vector store with lazy initialization
* **FR-004**: System MUST connect to Ollama models llama3:8b and nomic-embed-text
* **FR-005**: System MUST provide a GET / endpoint for health checks
* **FR-006**: System MUST define ChatRequest, ChatResponse, AddKnowledgeRequest, and FeedbackRequest Pydantic models
* **FR-007**: System MUST build a RAG chain using LangChain LCEL with retriever, prompt, model, and output_parser
* **FR-008**: System MUST provide a POST /chat endpoint that accepts questions and returns answers
* **FR-009**: System MUST retrieve relevant context from FAISS for user questions
* **FR-010**: System MUST generate answers using llama3:8b model with retrieved context
* **FR-011**: System MUST provide a POST /upload endpoint that accepts file uploads in multiple formats (PDF, TXT, DOCX, PPTX, XLSX, CSV, images)
* **FR-012**: System MUST extract text content from uploaded files using appropriate libraries
* **FR-013**: System MUST split uploaded documents into chunks and store them in FAISS
* **FR-014**: System MUST provide a GET /documents endpoint that returns a list of uploaded documents
* **FR-015**: System MUST provide a POST /upload-text endpoint for direct text input
* **FR-016**: System MUST provide a POST /add-knowledge endpoint for programmatic knowledge addition
* **FR-017**: System MUST implement SwiftFixPro FAQ knowledge base with 46+ categorized Q&A pairs
* **FR-018**: System MUST support conversation memory for multi-turn interactions
* **FR-019**: System MUST provide feedback collection system for response quality improvement
* **FR-020**: System MUST support Docker deployment with Miniconda environment
* **FR-021**: System MUST provide comprehensive API testing and validation tools

### Key Entities *(include if feature involves data)*

* **Question**: User input text representing the query
* **Answer**: Generated response text from the LLM
* **Document Chunk**: Portion of private document stored as vector embedding
* **Vector Embedding**: Numerical representation of document chunks for similarity search
* **Knowledge Entry**: Structured Q&A pair from FAQ knowledge base
* **Conversation Memory**: Stored conversation history for multi-turn interactions
* **Feedback Entry**: User feedback on response quality and accuracy

## Success Criteria *(mandatory)*

### Measurable Outcomes

* **SC-001**: Users receive chat responses within 2 seconds for questions with available context
* **SC-002**: System correctly retrieves relevant document context for 95% of test questions
* **SC-003**: API endpoints return proper HTTP status codes and structured responses
* **SC-004**: System successfully connects to all required components (Ollama, FAISS) on startup
* **SC-005**: SwiftFixPro FAQ knowledge base contains 46+ properly categorized Q&A pairs
* **SC-006**: Model validation confirms llama3:8b is properly loaded and responding
* **SC-007**: Docker deployment successfully runs multi-service setup with health checks
