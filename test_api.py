#!/usr/bin/env python3
"""Test script for the GPT-Neo RAG chatbot API."""

import requests
import json
import time

def test_chat_api():
    """Test the chat API with a simple question."""
    base_url = "http://localhost:8000"

    # Test data
    test_question = "What is SwiftFixPro?"
    conversation_id = "test_conversation_123"

    payload = {
        "question": test_question,
        "conversation_id": conversation_id
    }

    try:
        print("Testing chat API...")
        response = requests.post(f"{base_url}/chat", json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print("✅ Chat API test successful!")
            print(f"Question: {test_question}")
            print(f"Answer: {result['answer'][:200]}...")
            print(f"Conversation ID: {result['conversation_id']}")
            return True
        else:
            print(f"❌ Chat API test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_upload_text():
    """Test uploading text to the knowledge base."""
    base_url = "http://localhost:8000"

    test_text = """
    SwiftFixPro is a comprehensive property maintenance service that specializes in:
    - Emergency repairs and maintenance
    - Property inspections and assessments
    - Preventive maintenance programs
    - 24/7 emergency response
    - Licensed and insured technicians
    """

    payload = {
        "text": test_text
    }

    try:
        print("\nTesting text upload API...")
        response = requests.post(f"{base_url}/upload-text", json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print("✅ Text upload test successful!")
            print(f"Message: {result['message']}")
            return True
        else:
            print(f"❌ Text upload test failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting GPT-Neo RAG Chatbot API Tests")
    print("=" * 50)

    # Note: This test assumes the API is already running
    # In a real scenario, you'd start the server in a separate process

    success_count = 0
    total_tests = 2

    # Test upload first to add some knowledge
    if test_upload_text():
        success_count += 1
        time.sleep(2)  # Wait for processing

    # Test chat
    if test_chat_api():
        success_count += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 All tests passed! GPT-Neo RAG chatbot is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")