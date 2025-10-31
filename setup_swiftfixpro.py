#!/usr/bin/env python3
"""
Add SwiftFixPro Knowledge to Chatbot
Loads scraped content and adds it to the knowledge base.
"""

import requests
import json
import sys

def add_swiftfixpro_knowledge():
    """Add SwiftFixPro website content to the knowledge base."""

    # Load the scraped knowledge
    try:
        with open("swiftfixpro_knowledge.txt", 'r', encoding='utf-8') as f:
            knowledge_content = f.read()
    except FileNotFoundError:
        print("Error: swiftfixpro_knowledge.txt not found. Please run the scraper first.")
        return False

    if not knowledge_content.strip():
        print("Error: No content found in knowledge file.")
        return False

    # Split content into manageable chunks
    chunks = knowledge_content.split("---")
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    print(f"Found {len(chunks)} content chunks to add.")

    # Add each chunk to the knowledge base
    base_url = "http://localhost:8000"
    added_chunks = 0

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 50:  # Skip very small chunks
            continue

        payload = {
            "text": chunk,
            "source": "swiftfixpro_website",
            "category": "company_info"
        }

        try:
            response = requests.post(f"{base_url}/add-knowledge", json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                added_chunks += result.get('chunks_added', 0)
                print(f"✓ Added chunk {i+1}/{len(chunks)} ({result.get('chunks_added', 0)} sub-chunks)")
            else:
                print(f"✗ Failed to add chunk {i+1}: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"✗ Error adding chunk {i+1}: {str(e)}")

    print(f"\nSuccessfully added {added_chunks} total chunks to the knowledge base!")
    return True

def update_ai_prompt():
    """Update the AI system prompt to focus on SwiftFixPro context."""

    swiftfixpro_prompt = """
You are SwiftBot, the AI assistant for SwiftFixPro - a leading technology solutions company.

SwiftFixPro specializes in:
- Software development and consulting
- Digital transformation solutions
- IT infrastructure management
- Cloud services and migration
- Custom application development
- Technology training and support

When answering questions:
1. Always identify yourself as SwiftBot, the SwiftFixPro assistant
2. Focus on information from SwiftFixPro's website and services
3. Be helpful, professional, and knowledgeable about technology solutions
4. If you don't have specific information, suggest contacting SwiftFixPro directly
5. Emphasize SwiftFixPro's expertise and capabilities
6. Use conversational, friendly language while maintaining professionalism

Remember: You represent SwiftFixPro and should reflect their brand values of innovation, reliability, and customer satisfaction.
"""

    payload = {
        "text": swiftfixpro_prompt,
        "source": "system_prompt",
        "category": "ai_personality"
    }

    try:
        response = requests.post("http://localhost:8000/add-knowledge", json=payload, timeout=10)
        if response.status_code == 200:
            print("✓ AI personality updated to focus on SwiftFixPro")
            return True
        else:
            print(f"✗ Failed to update AI personality: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error updating AI personality: {str(e)}")
        return False

def test_swiftfixpro_knowledge():
    """Test that the SwiftFixPro knowledge is working."""

    test_questions = [
        "What is SwiftFixPro?",
        "What services does SwiftFixPro offer?",
        "Tell me about SwiftFixPro's expertise",
        "Who are you and what company do you represent?"
    ]

    print("\nTesting SwiftFixPro knowledge:")
    print("=" * 40)

    for question in test_questions:
        payload = {
            "question": question,
            "conversation_id": "swiftfixpro_test"
        }

        try:
            response = requests.post("http://localhost:8000/chat", json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                print(f"\nQ: {question}")
                print(f"A: {result['answer'][:200]}...")
            else:
                print(f"✗ Failed to get answer for: {question}")
        except Exception as e:
            print(f"✗ Error testing question '{question}': {str(e)}")

def main():
    """Main function to set up SwiftFixPro knowledge."""

    print("SwiftFixPro Knowledge Setup")
    print("=" * 30)

    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server is not running on http://localhost:8000")
            print("Please start the server first with: python main.py")
            return
    except:
        print("❌ Cannot connect to backend server on http://localhost:8000")
        print("Please start the server first with: python main.py")
        return

    print("✓ Backend server is running")

    # Add SwiftFixPro knowledge
    print("\nAdding SwiftFixPro website knowledge...")
    if add_swiftfixpro_knowledge():
        print("✓ Knowledge base updated with SwiftFixPro content")

        # Update AI personality
        print("\nUpdating AI personality for SwiftFixPro...")
        update_ai_prompt()

        # Test the knowledge
        print("\nTesting the updated knowledge...")
        test_swiftfixpro_knowledge()

        print("\n🎉 SwiftFixPro AI assistant setup complete!")
        print("Your chatbot now specializes in SwiftFixPro services and information.")

    else:
        print("❌ Failed to add SwiftFixPro knowledge")
        sys.exit(1)

if __name__ == "__main__":
    main()