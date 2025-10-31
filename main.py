from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from docx import Document as DocxDocument
from pptx import Presentation
import pandas as pd
import pytesseract
from PIL import Image
import json
from datetime import datetime

# Feedback storage - define before loading
feedback_store = []

# Load existing feedback on startup
try:
    if os.path.exists("feedback.jsonl"):
        with open("feedback.jsonl", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    feedback_store.append(json.loads(line.strip()))
except Exception as e:
    print(f"Warning: Could not load existing feedback: {e}")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003",
        "http://localhost:3004", "http://localhost:3005", "http://localhost:3006", "http://localhost:3007",
        "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002", "http://127.0.0.1:3003",
        "http://127.0.0.1:3004", "http://127.0.0.1:3005", "http://127.0.0.1:3006", "http://127.0.0.1:3007"
    ],  # React dev server origins (ports 3000-3007)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
llm = OllamaLLM(model="llama3.2", base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

# Initialize FAISS vector store
# Try to load existing FAISS index, or create new one
try:
    db = FAISS.load_local("./faiss_db", embeddings, allow_dangerous_deserialization=True)
except:
    # Create empty FAISS index if none exists
    from langchain_core.documents import Document
    empty_doc = Document(page_content="Initial document", metadata={"source": "init"})
    db = FAISS.from_documents([empty_doc], embeddings)

# Conversation memory store - simple dict-based approach
conversation_memories = {}

def get_or_create_memory(conversation_id: str):
    """Get or create conversation memory for a specific conversation."""
    if conversation_id not in conversation_memories:
        conversation_memories[conversation_id] = []
    return conversation_memories[conversation_id]

def add_to_memory(conversation_id: str, user_message: str, ai_message: str):
    """Add a conversation turn to memory."""
    memory = get_or_create_memory(conversation_id)
    memory.append({"user": user_message, "ai": ai_message})
    # Keep only last 10 conversations to prevent memory bloat
    if len(memory) > 10:
        memory.pop(0)

class ChatRequest(BaseModel):
    question: str
    conversation_id: str = "default"  # Allow multiple conversation threads

class ChatResponse(BaseModel):
    answer: str
    conversation_id: str

class FeedbackRequest(BaseModel):
    conversation_id: str
    question: str
    answer: str
    rating: int  # 1-5 scale
    feedback: str = ""  # Optional user feedback

class AddKnowledgeRequest(BaseModel):
    text: str
    source: str = "user_input"
    category: str = "general"

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = DocxDocument(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_pptx(file_path: str) -> str:
    """Extract text from a PPTX file."""
    prs = Presentation(file_path)
    full_text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text.append(shape.text)
    return '\n'.join(full_text)

def extract_text_from_excel(file_path: str) -> str:
    """Extract text from Excel files (XLSX/CSV)."""
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    return df.to_string()

def extract_text_from_image(file_path: str) -> str:
    """Extract text from images using OCR."""
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error extracting text from image: {str(e)}"

def extract_text_from_file(file_path: str, file_type: str) -> str:
    """Dispatch to appropriate extractor based on file type."""
    if file_type == 'pdf':
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return '\n'.join([doc.page_content for doc in documents])
    elif file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    elif file_type == 'pptx':
        return extract_text_from_pptx(file_path)
    elif file_type in ['xlsx', 'xls', 'csv']:
        return extract_text_from_excel(file_path)
    elif file_type in ['png', 'jpg', 'jpeg', 'bmp', 'tiff']:
        return extract_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

retriever = db.as_retriever(search_kwargs={"k": 10})  # Retrieve top 10 most similar chunks

# Create conversational RAG chain
def create_conversational_chain(memory):
    """Create a conversational RAG chain with memory."""
    # Format chat history for the prompt
    chat_history_text = ""
    if memory:
        for turn in memory[-5:]:  # Use last 5 turns
            chat_history_text += f"User: {turn['user']}\nAssistant: {turn['ai']}\n"

    template = f"""You are SwiftBot, the AI assistant for SwiftFixPro property maintenance services.

STRICT RULES - YOU MUST FOLLOW THESE EXACTLY:
1. ONLY answer using information explicitly found in the Context provided below
2. If the question cannot be answered using ONLY the Context, respond with: "I'm sorry, I don't have information about that in my knowledge base. Please contact SwiftFixPro directly for more details."
3. DO NOT add, invent, or assume any information not in the Context
4. DO NOT use any pre-trained knowledge about SwiftFixPro or property services
5. SwiftFixPro provides property maintenance services - ONLY mention services listed in the Context
6. If asked about services not in the Context, say you don't have that information

Context: {{context}}
Chat History: {chat_history_text}

Question: {{question}}
Answer:"""

    prompt_template = ChatPromptTemplate.from_template(template)

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return chain

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and add it to the vector database. Supports PDF, TXT, DOCX, PPTX, XLSX, CSV, and images."""
    try:
        # Determine file type
        file_extension = os.path.splitext(file.filename)[1].lower().lstrip('.')
        supported_types = ['pdf', 'txt', 'docx', 'pptx', 'xlsx', 'xls', 'csv', 'png', 'jpg', 'jpeg', 'bmp', 'tiff']
        
        if file_extension not in supported_types:
            return {"error": f"Unsupported file type: {file_extension}. Supported types: {', '.join(supported_types)}"}

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Extract text using the appropriate method
        try:
            text_content = extract_text_from_file(temp_file_path, file_extension)
        except Exception as e:
            os.unlink(temp_file_path)
            return {"error": f"Failed to extract text from {file.filename}: {str(e)}"}

        # Create a document from the extracted text
        from langchain_core.documents import Document
        document = Document(page_content=text_content, metadata={"source": file.filename})
        
        # Split the document
        chunks = text_splitter.split_documents([document])

        # Add to vector database
        global db
        db.add_documents(chunks)

        # Save FAISS index
        db.save_local("./faiss_db")

        # Clean up temp file
        os.unlink(temp_file_path)

        return {"message": f"Successfully uploaded {file.filename} and added {len(chunks)} chunks to the database."}

    except Exception as e:
        return {"error": f"Failed to process document: {str(e)}"}

class UploadTextRequest(BaseModel):
    text: str

@app.post("/upload-text")
async def upload_text(request: UploadTextRequest):
    """Upload text content directly and add it to the vector database."""
    try:
        # Create a document from the text
        from langchain_core.documents import Document
        document = Document(page_content=request.text)
        
        # Split the document
        chunks = text_splitter.split_documents([document])
        
        # Add to vector database
        global db
        db.add_documents(chunks)
        
        # Save FAISS index
        db.save_local("./faiss_db")
        
        return {"message": f"Successfully uploaded text and added {len(chunks)} chunks to the database."}
    
    except Exception as e:
        return {"error": f"Failed to process text: {str(e)}"}

@app.get("/")
def read_root():
    return {"status": "RAG API is online"}

@app.get("/documents")
async def list_documents():
    """Get a list of uploaded documents."""
    try:
        # FAISS doesn't have a direct get() method like Chroma
        # We'll return a simple message for now
        return {"documents": ["FAISS vector store - documents loaded"], "note": "Document listing not fully implemented for FAISS"}
    
    except Exception as e:
        return {"error": f"Failed to retrieve documents: {str(e)}", "documents": []}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat with the AI using conversational memory."""
    try:
        # Get conversation memory
        memory = get_or_create_memory(request.conversation_id)

        # Create conversational chain
        chain = create_conversational_chain(memory)

        # Get response
        response = await chain.ainvoke(request.question)

        # Add to memory
        add_to_memory(request.conversation_id, request.question, response)

        return ChatResponse(answer=response, conversation_id=request.conversation_id)

    except Exception as e:
        return ChatResponse(
            answer=f"I apologize, but I encountered an error: {str(e)}. Please try again.",
            conversation_id=request.conversation_id
        )

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback on a chat response to help improve the system."""
    try:
        feedback_entry = {
            "conversation_id": request.conversation_id,
            "question": request.question,
            "answer": request.answer,
            "rating": request.rating,
            "feedback": request.feedback,
            "timestamp": datetime.now().isoformat()
        }

        feedback_store.append(feedback_entry)

        # Save feedback to file for persistence
        with open("feedback.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(feedback_entry) + "\n")

        return {"message": "Thank you for your feedback! It will help improve the system."}

    except Exception as e:
        return {"error": f"Failed to save feedback: {str(e)}"}

@app.post("/add-knowledge")
async def add_knowledge(request: AddKnowledgeRequest):
    """Add new knowledge directly from user input to the knowledge base."""
    try:
        # Create a document from the user input
        from langchain_core.documents import Document
        document = Document(
            page_content=request.text,
            metadata={
                "source": request.source,
                "category": request.category,
                "added_by": "user",
                "timestamp": datetime.now().isoformat()
            }
        )

        # Split the document
        chunks = text_splitter.split_documents([document])

        # Add to vector database
        global db
        db.add_documents(chunks)

        # Save FAISS index
        db.save_local("./faiss_db")

        return {
            "message": f"Successfully added knowledge and created {len(chunks)} chunks.",
            "chunks_added": len(chunks),
            "source": request.source,
            "category": request.category
        }

    except Exception as e:
        return {"error": f"Failed to add knowledge: {str(e)}"}

@app.get("/conversations")
async def list_conversations():
    """Get a list of active conversation IDs."""
    return {"conversations": list(conversation_memories.keys())}

@app.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear the memory for a specific conversation."""
    if conversation_id in conversation_memories:
        del conversation_memories[conversation_id]
        return {"message": f"Cleared conversation memory for {conversation_id}"}
    else:
        return {"error": f"Conversation {conversation_id} not found"}

@app.get("/feedback")
async def get_feedback(limit: int = 10):
    """Get recent feedback entries."""
    return {"feedback": feedback_store[-limit:] if feedback_store else []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)