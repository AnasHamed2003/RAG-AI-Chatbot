import requests
import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the scraped SwiftFixPro content
with open('swiftfixpro_js_knowledge.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split content into pages (separated by ---)
pages = content.split('---\n')

# Filter for property maintenance related content only
property_maintenance_pages = []
for page in pages:
    if any(keyword in page.lower() for keyword in [
        'property maintenance', 'repair', 'services', 'painting', 'electrical',
        'plumbing', 'carpentry', 'flooring', 'appliance', 'furniture',
        'moving', 'renovation', 'safety', 'security', 'cleaning', 'elderly care'
    ]) and 'software' not in page.lower() and 'digital' not in page.lower() and 'it infrastructure' not in page.lower():
        property_maintenance_pages.append(page.strip())

print(f"Found {len(property_maintenance_pages)} property maintenance related pages")

# Create documents from filtered content
documents = []
for page in property_maintenance_pages:
    if page.strip():
        doc = Document(
            page_content=page,
            metadata={"source": "swiftfixpro_property_maintenance", "type": "property_services"}
        )
        documents.append(doc)

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks from property maintenance content")

# Add to knowledge base via API
base_url = "http://localhost:8000"

for i, chunk in enumerate(chunks):
    payload = {
        "text": chunk.page_content,
        "source": "swiftfixpro_property_maintenance",
        "category": "property_services"
    }

    try:
        response = requests.post(f"{base_url}/add-knowledge", json=payload)
        if response.status_code == 200:
            print(f"Added chunk {i+1}/{len(chunks)}")
        else:
            print(f"Failed to add chunk {i+1}: {response.text}")
    except Exception as e:
        print(f"Error adding chunk {i+1}: {e}")

print("Property maintenance knowledge base setup complete!")