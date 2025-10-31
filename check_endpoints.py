import requests

# Check for sitemap or robots.txt
base_url = 'https://www.swiftfixpro.com'
paths = ['/sitemap.xml', '/robots.txt', '/api', '/docs']

for path in paths:
    try:
        response = requests.get(f'{base_url}{path}', timeout=10)
        if response.status_code == 200:
            print(f'Found: {path} ({len(response.text)} chars)')
            if 'sitemap' in path.lower():
                print('Sitemap content:')
                print(response.text[:500])
        else:
            print(f'Not found: {path} ({response.status_code})')
    except Exception as e:
        print(f'Error checking {path}: {e}')