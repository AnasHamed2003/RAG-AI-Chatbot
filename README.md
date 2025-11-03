# SwiftFixPro Chatbot API

A FastAPI-based RAG chatbot for SwiftFixPro property maintenance services using Ollama.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Ollama is running with llama3:8b and nomic-embed-text models:
   ```bash
   ollama pull llama3:8b
   ollama pull nomic-embed-text
   ollama serve
   ```

3. Run locally:
   ```bash
   # Using conda (recommended)
   conda run python main.py
   
   # Or directly (if environment is properly configured)
   python main.py
   ```

4. Or with Docker (includes Ollama):
   ```bash
   docker-compose up --build
   ```
   This will automatically pull and run Ollama with the required models.

## Deployment on Your Own Server

### Prerequisites
- Server with Docker installed
- Ollama installed and running on the server
- Models pulled: `llama3:8b` and `nomic-embed-text`

### Step 1: Install Ollama on Your Server
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3:8b
ollama pull nomic-embed-text

# Start Ollama service
ollama serve
```

### Step 2: Deploy the Application
```bash
# Clone your repository
git clone <your-repo-url>
cd <your-project-directory>

# Build and run with Docker
docker-compose up --build -d

# Or run directly (if Python environment is set up)
pip install -r requirements.txt
conda run python main.py
```

### Step 3: Configure Firewall/Reverse Proxy
- Open port 8000 on your server firewall
- Optionally set up Nginx/Apache as reverse proxy for domain access
- For HTTPS, configure SSL certificates

### Step 4: Access Your API
Your API will be available at `http://your-server-ip:8000`

## Alternative: Cloud Deployment with Ollama

If you prefer cloud deployment while keeping Ollama:

### Railway with Ollama
1. Deploy Ollama separately on Railway or another service
2. Update the Ollama URL in your code to point to the cloud Ollama instance
3. Deploy your FastAPI app normally

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Chat with the bot
- `POST /upload` - Upload documents
- `POST /add-knowledge` - Add knowledge manually
- `GET /documents` - List documents
- `POST /feedback` - Submit feedback

## CORS Configuration

The API allows requests from localhost ports 3000-3007 for development. Update CORS origins in production as needed.