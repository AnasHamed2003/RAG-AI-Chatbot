import requests
import json

# Example of how to add SwiftFixPro knowledge manually
knowledge_text = '''
# SwiftFixPro Company Information

SwiftFixPro is a leading technology solutions company specializing in:
- Software development and custom application development
- Digital transformation services
- IT infrastructure management
- Cloud services and migration
- Property management software solutions
- Maintenance service platforms
- Product purchasing systems
- Recommendation and rewards systems

## Services Offered:
1. Property Management Services - Complete solutions for property management companies
2. Maintenance & Repair Services - Streamlined maintenance request and tracking systems
3. Product Purchasing Platform - Integrated purchasing solutions
4. Rewards & Recommendation System - Incentive programs for users and partners

## Key Features:
- User-friendly interface for property managers
- Real-time maintenance tracking
- Automated purchasing workflows
- Performance analytics and reporting
- Mobile-responsive design
- Multi-language support (including Chinese)

## Contact Information:
Website: https://www.swiftfixpro.com
'''

url = 'http://localhost:8000/add-knowledge'
data = {
    'text': knowledge_text,
    'source': 'swiftfixpro_website_manual',
    'category': 'company_info'
}

try:
    response = requests.post(url, json=data)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
    print('Make sure the FastAPI server is running with: conda run python main.py')