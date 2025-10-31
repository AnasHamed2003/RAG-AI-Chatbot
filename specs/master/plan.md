# Implementation Plan: Build the FastAPI "Brain" (main.py)

**Branch**: `master` | **Date**: October 29, 2025 | **Spec**: specs/master/spec.md
**Input**: Feature specification from `/specs/master/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a FastAPI application (main.py) that serves as the RAG API "Brain" for the private chatbot, integrating with ChromaDB vector store and Ollama models using LangChain LCEL.

## Technical Context

**Language/Version**: Python NEEDS CLARIFICATION (likely 3.11 or latest LTS)  
**Primary Dependencies**: FastAPI, LangChain, Ollama, ChromaDB  
**Storage**: ChromaDB (vector database for document embeddings)  
**Testing**: pytest NEEDS CLARIFICATION  
**Target Platform**: Linux server (self-hosted)  
**Project Type**: single (web API)  
**Performance Goals**: NEEDS CLARIFICATION (e.g., <2s response time for chat queries)  
**Constraints**: NEEDS CLARIFICATION (e.g., open-source only, local execution)  
**Scale/Scope**: NEEDS CLARIFICATION (e.g., single user, local deployment)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Since constitution.md is a template with placeholders, no specific gates are defined. Assuming compliance with general best practices.

## Project Structure

### Documentation (this feature)

```text
specs/master/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
main.py          # FastAPI app with chat endpoint
requirements.txt # Python dependencies
chroma_db/       # Existing vector store directory
```

**Structure Decision**: Single file application with main.py as the entry point, following the existing project structure.

## Complexity Tracking

No violations identified.

## Phase 0: Outline & Research

Extract unknowns from Technical Context:

- Python version: Research latest stable version compatible with FastAPI, LangChain, Ollama, ChromaDB
- Testing framework: Research pytest setup for FastAPI apps
- Performance goals: Research typical response times for RAG chatbots
- Constraints: Confirm all tools are open-source and support local execution
- Scale/Scope: Determine expected usage (single user, local)

Generate research.md with findings.

## Phase 1: Design & Contracts

Extract entities from feature spec:

- ChatRequest: { question: string }
- ChatResponse: { answer: string }

Generate API contracts:

- GET / : Health check
- POST /chat : { question: string } -> { answer: string }

Generate data-model.md, contracts/, quickstart.md

Update agent context.

Re-evaluate Constitution Check.
