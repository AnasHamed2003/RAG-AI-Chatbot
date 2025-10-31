Goal: Build the FastAPI "Brain" (`main.py`)

1.  **Task 1: Setup and Connections:**
    * Create the `main.py` file with a basic FastAPI app.
    * Load the required Python libraries (FastAPI, LangChain, Ollama, ChromaDB).
    * Establish and verify the connections to the two core components:
        * Connect to the *existing* `./chroma_db` vector store.
        * Connect to the *Ollama* models (`llama3` and `nomic-embed-text`).
    * Create a simple `/` endpoint to confirm the server is running.

2.  **Task 2: Define Data Models:**
    * Use Pydantic (built into FastAPI) to create data models for:
        * `ChatRequest`: A class that expects a `question` string.
        * `ChatResponse`: A class that will send back an `answer` string.

3.  **Task 3: Build the RAG Chain:**
    * Use LangChain Expression Language (LCEL) to build the full RAG "chain."
    * This chain will define the flow: `input` -> `retriever` -> `prompt` -> `model` -> `output_parser`.
    * This is the core logic that orchestrates the entire RAG process.

4.  **Task 4: Create the Chat Endpoint:**
    * Create a new POST `/chat` endpoint.
    * This endpoint will use the Pydantic models (from Task 2) and the RAG chain (from Task 3).
    * It will receive a question, "invoke" the chain, and return the final answer.