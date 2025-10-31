import requests

# Check for common subpages
base_url = 'https://www.swiftfixpro.com'
common_pages = ['', '/about', '/services', '/products', '/contact', '/faq', '/pricing', '/blog', '/news', '/support', '/docs', '/api']

print('Checking for available pages:')
for page in common_pages:
    try:
        url = f'{base_url}{page}' if page else base_url
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f'✓ {url} ({len(response.text)} chars)')
        else:
            print(f'✗ {url} ({response.status_code})')
    except Exception as e:
        print(f'✗ {url} (Error: {e})')