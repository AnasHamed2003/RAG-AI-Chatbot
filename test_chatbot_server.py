#!/usr/bin/env python3
import requests

def test_chatbot():
    base_url = "http://localhost:8000"

    print("🧪 Testing SwiftFixPro Chatbot Knowledge Base Connection")
    print("=" * 60)

    # Test 1: Basic API connectivity
    print("\n1. Testing basic API connectivity...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test 2: Chat without specific knowledge
    print("\n2. Testing chat with general question...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "question": "What services do you offer?",
            "conversation_id": "server_test_001"
        })
        result = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Question: What services do you offer?")
        print(f"Answer: {result['answer'][:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Add specific knowledge
    print("\n3. Adding test knowledge...")
    try:
        response = requests.post(f"{base_url}/add-knowledge", json={
            "text": "SwiftFixPro provides emergency plumbing services 24/7, including burst pipe repairs, water damage cleanup, and toilet overflow fixes. We also offer HVAC maintenance and repair services.",
            "source": "server_test",
            "category": "emergency_services"
        })
        print(f"✅ Add knowledge status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 4: Chat with newly added knowledge
    print("\n4. Testing retrieval of added knowledge...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "question": "Do you provide emergency plumbing services?",
            "conversation_id": "server_test_002"
        })
        result = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Question: Do you provide emergency plumbing services?")
        print(f"Answer: {result['answer'][:200]}...")

        # Check if the answer mentions emergency services
        if "emergency" in result['answer'].lower() or "24/7" in result['answer'].lower():
            print("✅ SUCCESS: Knowledge base retrieved the added information!")
        else:
            print("⚠️  WARNING: Answer doesn't seem to use the added knowledge")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 5: Test another specific question
    print("\n5. Testing HVAC services...")
    try:
        response = requests.post(f"{base_url}/chat", json={
            "question": "What HVAC services do you offer?",
            "conversation_id": "server_test_003"
        })
        result = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Question: What HVAC services do you offer?")
        print(f"Answer: {result['answer'][:200]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 60)
    print("🎉 Test completed! Check the results above.")
    print("\nIf you see answers that reference the knowledge you added,")
    print("then the RAG system is working correctly!")

if __name__ == "__main__":
    test_chatbot()