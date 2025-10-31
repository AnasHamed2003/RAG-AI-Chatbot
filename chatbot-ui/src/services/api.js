// API integration functions for the RAG Chatbot

const API_BASE_URL = 'http://localhost:8000';

/**
 * Upload a file to the server
 * @param {File} file - The file to upload
 * @returns {Promise<Object>} - Upload response
 */
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Upload failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

/**
 * Upload text directly to the server
 * @param {string} text - The text content to upload
 * @returns {Promise<Object>} - Upload response
 */
export const uploadText = async (text) => {
  try {
    const response = await fetch(`${API_BASE_URL}/upload-text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Text upload failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Text upload error:', error);
    throw error;
  }
};

/**
 * Get list of uploaded documents
 * @returns {Promise<Object>} - Documents list response
 */
export const getDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents`);

    if (!response.ok) {
      throw new Error('Failed to fetch documents');
    }

    return await response.json();
  } catch (error) {
    console.error('Get documents error:', error);
    throw error;
  }
};

/**
 * Send a chat message and get response
 * @param {string} question - The question to ask
 * @returns {Promise<Object>} - Chat response
 */
export const sendChatMessage = async (question) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Chat request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Chat error:', error);
    throw error;
  }
};

/**
 * Check if the API server is running
 * @returns {Promise<Object>} - Health check response
 */
export const checkServerHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/`);

    if (!response.ok) {
      throw new Error('Server is not responding');
    }

    return await response.json();
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};