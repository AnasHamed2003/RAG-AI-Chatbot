import requests

# Check for potential API endpoints or other resources
base_url = 'https://www.swiftfixpro.com'

# Check for common API patterns
api_patterns = [
    '/api/v1', '/api', '/graphql', '/rest', '/data',
    '/content', '/pages', '/posts', '/wp-json', '/api/content'
]

print('Checking for API endpoints:')
for pattern in api_patterns:
    try:
        url = f'{base_url}{pattern}'
        response = requests.get(url, timeout=10)
        print(f'{url}: {response.status_code} ({len(response.text)} chars)')
        if response.status_code == 200 and len(response.text) > 100:
            print(f'  Content preview: {response.text[:200]}...')
    except Exception as e:
        print(f'{url}: Error - {e}')