import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DocumentList from './components/DocumentList';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleUploadSuccess = (result) => {
    setUploadStatus({ type: 'success', message: result.message });
    setRefreshTrigger(prev => prev + 1); // Trigger document list refresh

    // Clear status after 5 seconds
    setTimeout(() => setUploadStatus(null), 5000);
  };

  const handleUploadError = (error) => {
    setUploadStatus({ type: 'error', message: error });
    setTimeout(() => setUploadStatus(null), 5000);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧠 Private RAG Chatbot</h1>
        <p>Upload documents and chat with your private knowledge base</p>
      </header>

      <main className="App-main">
        <div className="upload-section">
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />

          {uploadStatus && (
            <div className={`status-message ${uploadStatus.type}`}>
              {uploadStatus.type === 'success' ? '✅' : '❌'} {uploadStatus.message}
            </div>
          )}
        </div>

        <div className="content-section">
          <div className="documents-panel">
            <DocumentList refreshTrigger={refreshTrigger} />
          </div>

          <div className="chat-panel">
            <ChatInterface />
          </div>
        </div>
      </main>

      <footer className="App-footer">
        <p>Built with FastAPI, LangChain, Ollama, and ChromaDB</p>
      </footer>
    </div>
  );
}

export default App;
