import requests
import json
import time

def add_knowledge_to_ai():
    """Add scraped SwiftFixPro content to the AI knowledge base."""

    # Read the scraped content
    try:
        with open('swiftfixpro_js_knowledge.txt', 'r', encoding='utf-8') as f:
            knowledge_content = f.read()
    except FileNotFoundError:
        print("❌ Error: swiftfixpro_js_knowledge.txt not found. Please run the scraper first.")
        return

    # Split into individual page contents
    pages = knowledge_content.split('---')

    print(f'📄 Found {len(pages)} pages of content to add to knowledge base')
    print('🚀 Starting to add content to AI knowledge base...\n')

    # Add each page to the knowledge base
    url = 'http://localhost:8000/add-knowledge'
    successful_adds = 0

    for i, page_content in enumerate(pages):
        if not page_content.strip():  # Skip empty pages
            continue

        # Extract title from first line
        lines = page_content.strip().split('\n')
        title = lines[0].replace('# ', '') if lines[0].startswith('# ') else f'Page {i+1}'

        data = {
            'text': page_content.strip(),
            'source': f'swiftfixpro_website_js_page_{i+1}',
            'category': 'company_website'
        }

        try:
            print(f'📤 Adding page {i+1}: {title[:50]}...')
            response = requests.post(url, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                chunks_added = result.get('chunks_added', 0)
                print(f'✅ Successfully added page {i+1} ({chunks_added} chunks)')
                successful_adds += 1
            else:
                print(f'❌ Failed to add page {i+1}: HTTP {response.status_code}')
                print(f'   Response: {response.text}')

        except requests.exceptions.ConnectionError:
            print(f'❌ Connection error for page {i+1}. Is the FastAPI server running?')
            print('   Please start the server with: conda run python main.py')
            return
        except Exception as e:
            print(f'❌ Error adding page {i+1}: {e}')

        # Small delay to be respectful
        time.sleep(0.5)

    print(f'\n🎉 Successfully added {successful_adds} out of {len([p for p in pages if p.strip()])} pages to the AI knowledge base!')
    print('🤖 Your chatbot now has comprehensive knowledge about SwiftFixPro!')
    print('\n💡 You can now ask questions like:')
    print('   - "What services does SwiftFixPro offer?"')
    print('   - "How do I book a service?"')
    print('   - "What is the Agent Referral Program?"')
    print('   - "How does CEA verification work?"')

if __name__ == "__main__":
    add_knowledge_to_ai()