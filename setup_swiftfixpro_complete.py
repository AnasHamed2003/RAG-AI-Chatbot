#!/usr/bin/env python3
"""
Complete SwiftFixPro Setup Script
1. Scrapes the website
2. Sets up the knowledge base
3. Configures the AI personality
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}")
    print("-" * 40)

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Complete SwiftFixPro setup process."""

    print("🚀 SwiftFixPro AI Assistant Setup")
    print("=" * 50)

    # Step 1: Get website URL
    website_url = input("Enter SwiftFixPro website URL (e.g., https://swiftfixpro.com): ").strip()
    if not website_url:
        print("❌ Website URL is required")
        return

    # Step 2: Start the backend server
    print("\n📡 Starting backend server...")
    server_process = subprocess.Popen([
        "conda", "run", "-n", "base", "python", "main.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    import time
    time.sleep(3)  # Wait for server to start

    # Check if server is running
    import requests
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server failed to start")
            server_process.terminate()
            return
    except:
        print("❌ Cannot connect to backend server")
        server_process.terminate()
        return

    print("✓ Backend server is running")

    # Step 3: Run the scraper
    print("\n🕷️  Scraping SwiftFixPro website...")

    # Create a simple scraping script for the URL
    scraper_code = f'''
import requests
from bs4 import BeautifulSoup
import json

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "SwiftFixPro Page"

        # Extract main content
        content = ""
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
            text = tag.get_text().strip()
            if text and len(text) > 10:
                content += text + " "

        return {{
            'title': title_text,
            'content': content.strip(),
            'url': url
        }}
    except Exception as e:
        return None

# Scrape the main page
result = scrape_page("{website_url}")
if result:
    with open("swiftfixpro_content.json", 'w') as f:
        json.dump([result], f)
    print("Scraped content saved")
else:
    print("Failed to scrape content")
'''

    with open("temp_scraper.py", 'w') as f:
        f.write(scraper_code)

    if run_command("conda run -n base python temp_scraper.py", "Running website scraper"):
        # Clean up temp file
        os.remove("temp_scraper.py")
    else:
        server_process.terminate()
        return

    # Step 4: Process scraped content
    print("\n📝 Processing scraped content...")

    try:
        with open("swiftfixpro_content.json", 'r') as f:
            scraped_data = json.load(f)

        knowledge_text = ""
        for page in scraped_data:
            knowledge_text += f"# {{page['title']}}\n\n{{page['content']}}\n\n---\n\n"

        with open("swiftfixpro_knowledge.txt", 'w', encoding='utf-8') as f:
            f.write(knowledge_text)

        print("✓ Content processed and saved")

    except Exception as e:
        print(f"❌ Failed to process content: {{e}}")
        server_process.terminate()
        return

    # Step 5: Add knowledge to the system
    print("\n🧠 Adding knowledge to AI system...")

    setup_code = '''
import requests

# Load knowledge
with open("swiftfixpro_knowledge.txt", 'r', encoding='utf-8') as f:
    knowledge = f.read()

# Add to knowledge base
payload = {
    "text": knowledge,
    "source": "swiftfixpro_website",
    "category": "company_info"
}

response = requests.post("http://localhost:8000/add-knowledge", json=payload)
print(f"Knowledge addition: {{response.status_code}}")

# Add AI personality
personality = """
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
2. Focus on information from SwiftFixPro website and services
3. Be helpful, professional, and knowledgeable about technology solutions
4. If you don\'t have specific information, suggest contacting SwiftFixPro directly
5. Emphasize SwiftFixPro\'s expertise and capabilities
6. Use conversational, friendly language while maintaining professionalism

Remember: You represent SwiftFixPro and should reflect their brand values of innovation, reliability, and customer satisfaction.
"""

payload2 = {
    "text": personality,
    "source": "system_prompt",
    "category": "ai_personality"
}

response2 = requests.post("http://localhost:8000/add-knowledge", json=payload2)
print(f"Personality update: {{response2.status_code}}")
'''

    with open("temp_setup.py", 'w') as f:
        f.write(setup_code)

    if run_command("conda run -n base python temp_setup.py", "Setting up AI knowledge and personality"):
        os.remove("temp_setup.py")
    else:
        server_process.terminate()
        return

    # Step 6: Test the setup
    print("\n🧪 Testing SwiftFixPro AI assistant...")

    test_code = '''
import requests

# Test questions
questions = [
    "What is SwiftFixPro?",
    "What services do you offer?",
    "Who are you?"
]

for question in questions:
    payload = {
        "question": question,
        "conversation_id": "setup_test"
    }

    response = requests.post("http://localhost:8000/chat", json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Q: {{question}}")
        print(f"A: {{result['answer'][:100]}}...")
        print()
'''

    with open("temp_test.py", 'w') as f:
        f.write(test_code)

    run_command("conda run -n base python temp_test.py", "Testing AI responses")
    os.remove("temp_test.py")

    # Step 7: Final instructions
    print("\n🎉 SwiftFixPro AI Assistant Setup Complete!")
    print("=" * 50)
    print("Your AI assistant is now specialized for SwiftFixPro!")
    print()
    print("📁 Files created:")
    print("  - swiftfixpro_content.json (raw scraped data)")
    print("  - swiftfixpro_knowledge.txt (processed knowledge)")
    print()
    print("🚀 Your backend server is running on http://localhost:8000")
    print("💻 Start your React frontend: cd chatbot-ui && npm start")
    print()
    print("💡 The AI will now:")
    print("   - Introduce itself as SwiftBot from SwiftFixPro")
    print("   - Focus on SwiftFixPro services and information")
    print("   - Provide professional, helpful responses")
    print("   - Suggest contacting SwiftFixPro for specific inquiries")

    # Keep server running
    print("\n🔄 Backend server is still running. Press Ctrl+C to stop it when done.")
    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\n👋 Server stopped. Setup complete!")

if __name__ == "__main__":
    main()