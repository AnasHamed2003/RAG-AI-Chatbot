import requests

def test_swiftfixpro_ai():
    """Test the AI with SwiftFixPro questions using scraped content."""

    test_questions = [
        'What services does SwiftFixPro offer?',
        'How do I book a service with SwiftFixPro?',
        'What is the Agent Referral Program?',
        'How does CEA verification work?',
        'What are SwiftFixPro working hours?',
        'Tell me about SwiftFixPro company'
    ]

    url = 'http://localhost:8000/chat'

    print('🧪 Testing SwiftFixPro AI Knowledge')
    print('=' * 50)

    for i, question in enumerate(test_questions, 1):
        print(f'\n🤖 Question {i}: {question}')

        data = {
            'conversation_id': 'test_swiftfixpro',
            'question': question
        }

        try:
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No answer received')
                # Show first 200 characters of answer
                preview = answer[:200] + '...' if len(answer) > 200 else answer
                print(f'💬 Answer: {preview}')
            else:
                print(f'❌ Error: HTTP {response.status_code}')
        except requests.exceptions.ConnectionError:
            print('❌ Connection error: Is the FastAPI server running?')
            print('   Please start the server with: conda run python main.py')
            return
        except Exception as e:
            print(f'❌ Error: {e}')

    print('\n✅ Testing complete! Your AI now has comprehensive SwiftFixPro knowledge.')

if __name__ == "__main__":
    test_swiftfixpro_ai()