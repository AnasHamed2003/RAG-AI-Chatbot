# 🤖 SwiftFixPro RAG Chatbot API [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/) [![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/) [![Ollama](https://img.shields.io/badge/Ollama-llama3.8b-orange.svg)](https://ollama.ai/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive FastAPI-based RAG (Retrieval-Augmented Generation) chatbot for SwiftFixPro property maintenance services. Features advanced AI model, vector database, conversation memory, and comprehensive knowledge base.

## ✨ Key Features

- 🚀 **Advanced AI Model**: llama3:8b for superior response quality
- 🗄️ **Vector Database**: FAISS with lazy initialization for optimal performance
- 📚 **Knowledge Base**: Pre-loaded with 46+ SwiftFixPro FAQ Q&A pairs
- 💬 **Conversation Memory**: Multi-turn conversation support with context retention
- 📄 **Document Processing**: Support for PDF, DOCX, PPTX, XLSX, CSV, and image files
- ⭐ **Feedback System**: User feedback collection for continuous improvement
- 🐳 **Docker Deployment**: Production-ready containerized deployment
- 🧪 **Comprehensive Testing**: Built-in API and model validation tools

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

> **⚡ One-command setup with Docker:**

```bash
git clone https://github.com/AnasHamed2003/RAG-AI-Chatbot.git
cd RAG-AI-Chatbot
docker-compose up --build
```

That's it! Your chatbot will be running at `http://localhost:8000` with Ollama and all models pre-configured.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** with Miniconda (recommended)
- **Docker & Docker Compose** (for easy deployment)
- **Ollama** (for local model inference)
- **8GB+ RAM** (required for llama3:8b model)
- **Git** (for cloning the repository)

## 🛠️ Installation

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/AnasHamed2003/RAG-AI-Chatbot.git
cd RAG-AI-Chatbot

# Build and run with Docker
docker-compose up --build
```

### Option 2: Local Development

1. **Install Miniconda** (recommended for consistent Python environment):

   ```bash
   # Windows: Download from https://docs.conda.io/en/latest/miniconda.html
   # Linux/Mac: curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh | bash
   ```

2. **Create and activate conda environment**:

   ```bash
   conda create -n chatbot python=3.11
   conda activate chatbot
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Ollama**:

   ```bash
   # Install Ollama
   # Windows: Download from https://ollama.ai/download
   # Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh

   # Pull required models
   ollama pull llama3:8b
   ollama pull nomic-embed-text

   # Start Ollama service
   ollama serve
   ```

5. **Add SwiftFixPro Knowledge Base**:

   ```bash
   python add_faq_knowledge.py
   ```

## 🎯 Usage

### Start the Chatbot

```bash
# Using conda (recommended)
conda run python main.py

# Or directly
python main.py
```

The API will be available at `http://localhost:8000`

### Test the Chatbot

```bash
# Quick health check
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What services does SwiftFixPro offer?", "conversation_id": "test_001"}'
```

### Example API Usage

```python
import requests

# Chat with the bot
response = requests.post("http://localhost:8000/chat", json={
    "question": "Do you provide emergency plumbing services?",
    "conversation_id": "user_123"
})

print(response.json())
# {"answer": "Yes, SwiftFixPro provides 24/7 emergency plumbing services...", "conversation_id": "user_123"}
```

## 📡 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat` | Chat with the bot (supports conversation memory) |

### Document Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload documents (PDF, DOCX, PPTX, XLSX, CSV, images) |
| `POST` | `/upload-text` | Upload text content directly |
| `GET` | `/documents` | List uploaded documents |

### Knowledge Base Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/add-knowledge` | Add knowledge manually to vector database |
| `GET` | `/conversations` | List active conversation IDs |
| `DELETE` | `/conversation/{conversation_id}` | Clear specific conversation memory |

### Feedback System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/feedback` | Submit feedback on chat responses |
| `GET` | `/feedback` | Retrieve feedback history (admin use) |

### API Examples

#### Chat with Memory

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are your plumbing services?",
    "conversation_id": "user_session_1"
  }'
```

#### Upload Document

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

#### Add Knowledge

```bash
curl -X POST http://localhost:8000/add-knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "text": "SwiftFixPro offers 24/7 emergency services for plumbing and electrical issues.",
    "source": "manual",
    "category": "services"
  }'
```

## 🧪 Testing

### Run Comprehensive Tests

```bash
# Test the API endpoints
python test_chatbot_server_fixed.py
```

### Validate Model Setup

```bash
# Check model status and connectivity
./check_model_server.sh
```

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/

# Test chat functionality
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What services does SwiftFixPro offer?", "conversation_id": "test_001"}'

# Test document upload
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.pdf"
```

## 🌐 Deployment

### Server Deployment

1. **Install Ollama on your server**:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3:8b
   ollama pull nomic-embed-text
   ollama serve
   ```

2. **Deploy with Docker**:
   ```bash
   git clone https://github.com/AnasHamed2003/RAG-AI-Chatbot.git
   cd RAG-AI-Chatbot
   docker-compose up --build -d
   ```

3. **Configure firewall**:
   - Open port 8000 on your server firewall
   - Optionally set up Nginx/Apache as reverse proxy

### Environment Variables

Create a `.env` file for custom configuration:

```bash
OLLAMA_BASE_URL=http://localhost:11434
FAISS_DB_PATH=./faiss_db
FEEDBACK_FILE=feedback.jsonl
```

## 🐛 Troubleshooting

### Common Issues & Solutions

**❌ Model not loading:**

```bash
# Check Ollama status
ollama list

# Pull model if missing
ollama pull llama3:8b
```

**❌ Port already in use:**

```bash
# Kill existing processes
pkill -f "python main.py"
pkill -f ollama

# Or use different port
uvicorn main:app --host 0.0.0.0 --port 8001
```

**❌ Memory issues:**

- Ensure 8GB+ RAM available
- Reduce concurrent requests
- Consider using smaller model for testing

**❌ Docker issues:**

```bash
# Clean rebuild
docker-compose down
docker system prune -f
docker-compose up --build
```

### Debug Commands

```bash
# View application logs
docker-compose logs -f chatbot

# View Ollama logs
docker-compose logs -f ollama

# Test API manually
curl http://localhost:8000/
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Response Time** | <2 seconds for typical queries |
| **Memory Usage** | ~8GB RAM for llama3:8b model |
| **Concurrent Users** | Optimized for single-user deployment |
| **Knowledge Base** | 46+ pre-loaded SwiftFixPro Q&A pairs |
| **Model Size** | 8B parameters (llama3:8b) |

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Run tests**: `python test_chatbot_server_fixed.py`
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to the branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- 📖 **Documentation**: Check this README and inline code comments
- 🐛 **Issues**: [Open an issue](https://github.com/AnasHamed2003/RAG-AI-Chatbot/issues) on GitHub
- 💬 **Discussions**: Use [GitHub Discussions](https://github.com/AnasHamed2003/RAG-AI-Chatbot/discussions) for questions

### Quick Support Checklist

- [ ] Check the troubleshooting section above
- [ ] Review the API documentation
- [ ] Test with the provided validation scripts
- [ ] Check Docker and Ollama logs for errors
- [ ] Ensure you have 8GB+ RAM available

---

Built with ❤️ for SwiftFixPro property maintenance services

⭐ **Star this repo** if you find it helpful!

[📧 Contact](mailto:support@swiftfixpro.sg) • [🌐 Website](https://swiftfixpro.sg) • [🐛 Report Bug](https://github.com/AnasHamed2003/RAG-AI-Chatbot/issues)
 