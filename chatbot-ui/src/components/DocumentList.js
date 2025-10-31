import React, { useState, useEffect } from 'react';
import { getDocuments } from '../services/api';
import './DocumentList.css';

const DocumentList = ({ refreshTrigger }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await getDocuments();
      setDocuments(result.documents || []);
    } catch (err) {
      setError(err.message);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  const getFileIcon = (filename) => {
    const ext = filename.split('.').pop().toLowerCase();
    const iconMap = {
      pdf: '📄',
      txt: '📝',
      docx: '📃',
      pptx: '📊',
      xlsx: '📈',
      xls: '📈',
      csv: '📊',
      png: '🖼️',
      jpg: '🖼️',
      jpeg: '🖼️',
      bmp: '🖼️',
      tiff: '🖼️',
    };
    return iconMap[ext] || '📄';
  };

  if (loading) {
    return (
      <div className="document-list-container">
        <h3>Uploaded Documents</h3>
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading documents...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="document-list-container">
        <h3>Uploaded Documents</h3>
        <div className="error-message">
          <p>❌ Error loading documents: {error}</p>
          <button onClick={fetchDocuments} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="document-list-container">
      <div className="document-list-header">
        <h3>Uploaded Documents ({documents.length})</h3>
        <button onClick={fetchDocuments} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {documents.length === 0 ? (
        <div className="empty-state">
          <p>📂 No documents uploaded yet</p>
          <small>Upload some documents to get started with your knowledge base</small>
        </div>
      ) : (
        <div className="document-grid">
          {documents.map((doc, index) => (
            <div key={index} className="document-item">
              <div className="document-icon">
                {getFileIcon(doc)}
              </div>
              <div className="document-info">
                <div className="document-name" title={doc}>
                  {doc.length > 20 ? `${doc.substring(0, 20)}...` : doc}
                </div>
                <div className="document-type">
                  {doc.split('.').pop().toUpperCase()}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DocumentList;