# Implementation Plan: Private RAG Chatbot

**Branch**: `001-private-rag-chatbot` | **Date**: November 4, 2025 | **Spec**: specs/001-private-rag-chatbot/spec.md
**Input**: Feature specification from `/specs/001-private-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build the FastAPI "Brain" (main.py) with comprehensive document upload capabilities, SwiftFixPro FAQ knowledge base, conversation memory, feedback system, and Docker deployment with Miniconda environment. Upgraded to llama3:8b model and FAISS vector database for improved performance.

## Technical Context

**Language/Version**: Python 3.11 (Miniconda environment)  
**Primary Dependencies**: FastAPI, LangChain, Ollama, FAISS  
**Storage**: FAISS (vector database with lazy initialization)  
**Testing**: pytest, custom API testing scripts  
**Target Platform**: Linux server (Docker deployment)  
**Project Type**: single (web API with comprehensive features)  
**Performance Goals**: <2 seconds response time for chat queries  
**Constraints**: 100% open-source tools, local execution with Docker  
**Scale/Scope**: Single user, production server deployment  
**Model**: llama3:8b (upgraded from llama3.2)  
**Knowledge Base**: SwiftFixPro FAQ (46+ categorized Q&A pairs)  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution.md is a template with no specific rules defined. Assuming compliance with general development best practices.

## Project Structure

### Documentation (this feature)

```text
specs/001-private-rag-chatbot/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
main.py                 # FastAPI app with comprehensive features
requirements.txt        # Python dependencies for Miniconda
docker-compose.yml      # Multi-service Docker deployment
Dockerfile             # Miniconda-based container setup
init_ollama.sh         # Ollama model initialization script
faiss_db/              # FAISS vector database directory
feedback.jsonl         # User feedback storage
add_faq_knowledge.py   # FAQ knowledge base addition script
test_chatbot_server_fixed.py  # API testing script
check_model_server.sh  # Model validation script
README.md              # Deployment and usage documentation
```

**Structure Decision**: Single file application with main.py as the entry point, following the existing project structure for a simple API service.

## Complexity Tracking

No violations identified.

## Phase 0: Outline & Research

Resolved all technical decisions:

- Model: llama3:8b (upgraded from llama3.2 for better performance)
- Vector Database: FAISS with lazy initialization (changed from ChromaDB)
- Environment: Miniconda for consistent Python package management
- Deployment: Docker with multi-service setup (chatbot + Ollama)
- Knowledge Base: SwiftFixPro FAQ with 46+ categorized Q&A pairs
- Testing: Comprehensive API and model validation scripts

## Phase 1: Design & Contracts

Extract entities from feature spec:

- Question: user input text with conversation_id
- Answer: generated response text with conversation context
- Document Chunk: vectorized document portions in FAISS
- Vector Embedding: numerical representations for similarity search
- Knowledge Entry: structured Q&A from FAQ knowledge base
- Conversation Memory: stored multi-turn conversation history
- Feedback Entry: user ratings and comments on responses
- Uploaded File: user-uploaded document with metadata and processing

Generate API contracts:

- GET / : Health check
- POST /chat : Accept ChatRequest, return ChatResponse with conversation memory
- POST /upload : Accept file upload, return UploadResponse
- GET /documents : Return list of uploaded documents
- POST /upload-text : Accept text input, return UploadResponse
- POST /add-knowledge : Accept knowledge addition, return confirmation
- POST /feedback : Accept user feedback, return confirmation
- GET /feedback : Return feedback history
- GET /conversations : Return active conversation IDs
- DELETE /conversation/{id} : Clear specific conversation memory

Generate data-model.md, contracts/, quickstart.md

Update agent context.

Re-evaluate Constitution Check.
