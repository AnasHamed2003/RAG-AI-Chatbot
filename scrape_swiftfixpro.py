#!/usr/bin/env python3
"""
SwiftFixPro Website Scraper
Scrapes content from SwiftFixPro website and adds it to the knowledge base.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from urllib.parse import urljoin, urlparse
from typing import Set, List, Dict
import re

class SwiftFixProScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.visited_urls: Set[str] = set()
        self.scraped_content: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to SwiftFixPro domain."""
        parsed = urlparse(url)
        return parsed.netloc in ['swiftfixpro.com', 'www.swiftfixpro.com']

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove script and style content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace again
        text = re.sub(r'\s+', ' ', text.strip())
        return text

    def extract_main_content(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract main content from a webpage with multiple fallback strategies."""
        print(f"  Extracting content from: {url}")

        # Strategy 1: Try common content selectors
        content_selectors = [
            'main', '.content', '.main-content', '#content', '.post-content',
            '.entry-content', 'article', '.article-content', '.page-content',
            '.site-content', '#main', '.container', '.wrapper'
        ]

        content_text = ""

        # Try main content selectors first
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for elem in elements:
                    text = self.clean_text(str(elem))
                    if len(text) > 50:  # Only substantial content
                        content_text += text + " "
                        print(f"    ✓ Found content in selector '{selector}': {len(text)} chars")

        # Strategy 2: Extract from all paragraph and heading tags
        if not content_text or len(content_text) < 200:
            print("    Trying fallback: extracting from p, h1-h6, li tags")
            all_text = ""
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div']):
                text = tag.get_text().strip()
                if text and len(text) > 10 and not any(skip in text.lower() for skip in ['copyright', 'privacy', 'terms']):
                    all_text += text + " "

            if len(all_text) > len(content_text):
                content_text = all_text
                print(f"    ✓ Fallback extraction: {len(content_text)} chars")

        # Strategy 3: Extract from body if still no content
        if not content_text or len(content_text) < 100:
            print("    Trying fallback: extracting from body")
            body = soup.find('body')
            if body:
                body_text = self.clean_text(str(body))
                if len(body_text) > len(content_text):
                    content_text = body_text
                    print(f"    ✓ Body extraction: {len(content_text)} chars")

        # Strategy 4: Extract any text content
        if not content_text:
            print("    Trying fallback: extracting all text")
            all_text = soup.get_text()
            content_text = self.clean_text(all_text)
            print(f"    ✓ All text extraction: {len(content_text)} chars")

        # Extract title
        title = ""
        title_selectors = ['h1', 'title', '.page-title', '.entry-title', '.site-title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = self.clean_text(title_elem.get_text())
                if title:
                    print(f"    ✓ Found title: {title[:50]}...")
                    break

        # Fallback title
        if not title:
            title_elem = soup.find('title')
            if title_elem:
                title = self.clean_text(title_elem.get_text())
            else:
                title = "SwiftFixPro Page"

        # Extract meta description
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and meta_tag.get('content'):
            meta_desc = meta_tag['content']
            print(f"    ✓ Found meta description: {meta_desc[:50]}...")

        result = {
            'url': url,
            'title': title,
            'meta_description': meta_desc,
            'content': content_text.strip(),
            'word_count': len(content_text.split()) if content_text else 0,
            'char_count': len(content_text) if content_text else 0
        }

        print(f"    📊 Final result: {result['word_count']} words, {result['char_count']} chars")
        return result

    def scrape_page(self, url: str) -> Dict:
        """Scrape a single page."""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
            content = self.extract_main_content(soup, url)

            # Find links to other pages on the site
            links = soup.find_all('a', href=True)
            internal_links = []

            for link in links:
                href = link['href']
                full_url = urljoin(url, href)

                # Only include internal links
                if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                    # Avoid common non-content URLs
                    if not any(skip in full_url.lower() for skip in [
                        '#', 'javascript:', 'mailto:', '.jpg', '.png', '.gif', '.pdf', '.zip',
                        '/wp-admin/', '/wp-content/', '/wp-includes/', '/admin/', '/login'
                    ]):
                        internal_links.append(full_url)

            content['internal_links'] = list(set(internal_links))  # Remove duplicates

            return content

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def scrape_website(self, max_pages: int = 50) -> List[Dict]:
        """Scrape the entire website up to max_pages."""
        to_visit = [self.base_url]
        pages_scraped = 0

        while to_visit and pages_scraped < max_pages:
            current_url = to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            content = self.scrape_page(current_url)

            if content:
                # Be more lenient with content - accept anything with at least some text
                min_chars = 50  # Reduced from 100
                if content['char_count'] >= min_chars:
                    self.scraped_content.append(content)
                    pages_scraped += 1
                    print(f"✓ Scraped page {pages_scraped}: {content['title'][:50]}... ({content['word_count']} words, {content['char_count']} chars)")
                else:
                    print(f"⚠️ Skipped page (too short): {content['title'][:30]}... ({content['char_count']} chars)")

                # Add new links to visit (be more selective)
                for link in content.get('internal_links', []):
                    if (link not in self.visited_urls and
                        link not in to_visit and
                        pages_scraped < max_pages):
                        # Only add links that look like actual pages
                        if not any(skip in link for skip in ['.jpg', '.png', '.gif', '.pdf', '.zip', '.css', '.js']):
                            to_visit.append(link)
                            print(f"  Added to queue: {link}")

            # Be respectful to the server
            time.sleep(1)

        return self.scraped_content

    def scrape_subpages(self, subpages: List[str] = None) -> List[Dict]:
        """Scrape specific subpages of the website."""
        if subpages is None:
            # Default subpages to scrape
            subpages = [
                '',  # home page
                '/about',
                '/services',
                '/products',
                '/contact',
                '/faq',
                '/pricing',
                '/blog',
                '/news',
                '/support',
                '/docs'
            ]

        print(f"Scraping {len(subpages)} specific subpages from {self.base_url}...")

        for subpage in subpages:
            url = f"{self.base_url}{subpage}" if subpage else self.base_url

            if url in self.visited_urls:
                print(f"  Skipping already visited: {url}")
                continue

            print(f"\nScraping subpage: {url}")
            content = self.scrape_page(url)

            if content:
                # For subpages, be even more lenient since SPA content might be minimal
                min_chars = 20  # Very lenient for subpages
                if content['char_count'] >= min_chars:
                    self.scraped_content.append(content)
                    print(f"✓ Scraped subpage: {content['title'][:50]}... ({content['word_count']} words, {content['char_count']} chars)")
                else:
                    print(f"⚠️ Subpage too short: {content['title'][:30]}... ({content['char_count']} chars)")
                    # Still add it but mark as minimal
                    content['note'] = 'Minimal content - likely SPA placeholder'
                    self.scraped_content.append(content)

            self.visited_urls.add(url)
            time.sleep(1)  # Be respectful

        return self.scraped_content

    def save_to_json(self, filename: str = "swiftfixpro_content.json"):
        """Save scraped content to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_content, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.scraped_content)} pages to {filename}")

    def format_for_knowledge_base(self) -> str:
        """Format scraped content for addition to knowledge base."""
        formatted_content = []

        for page in self.scraped_content:
            page_content = f"""
# {page['title']}

URL: {page['url']}

{page['meta_description']}

{page['content']}
"""
            formatted_content.append(page_content.strip())

        return "\n\n---\n\n".join(formatted_content)

def simple_scrape_website(url: str) -> str:
    """Simple fallback scraper that extracts any available text."""
    try:
        import requests
        from bs4 import BeautifulSoup

        print(f"Simple scraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Extract all text
        text = soup.get_text()

        # Clean up the text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        cleaned_text = '\n'.join(lines)

        # Get title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "SwiftFixPro Website"

        # Get meta description
        meta_desc = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and meta_tag.get('content'):
            meta_desc = meta_tag['content']

        result = f"""# {title_text}

URL: {url}

Description: {meta_desc}

Content:
{cleaned_text}
"""

        print(f"Simple scrape successful: {len(cleaned_text)} characters")
        return result

    except Exception as e:
        print(f"Simple scrape failed: {e}")
        return f"# SwiftFixPro Website\n\nURL: {url}\n\nContent: Unable to extract content from website. Error: {str(e)}"
def main():
    """Main scraping function."""
    import sys

    # Get URL from command line argument or use default
    if len(sys.argv) > 1:
        website_url = sys.argv[1]
    else:
        website_url = "https://swiftfixpro.com"  # Default URL

    print(f"Starting to scrape: {website_url} and its subpages")
    print("=" * 60)

    # Scrape specific subpages
    scraper = SwiftFixProScraper(website_url)
    scraped_pages = scraper.scrape_subpages()

    if scraped_pages:
        print(f"\n✅ Successfully scraped {len(scraped_pages)} pages!")

        # Save raw data
        scraper.save_to_json()

        # Format for knowledge base
        knowledge_content = scraper.format_for_knowledge_base()
    else:
        print("\n❌ No pages were scraped successfully. Trying simple scraper...")

        # Fallback to simple scraper for main page
        knowledge_content = simple_scrape_website(website_url)

        # Save as JSON for consistency
        with open("swiftfixpro_content.json", 'w', encoding='utf-8') as f:
            json.dump([{
                'url': website_url,
                'title': 'SwiftFixPro Website',
                'content': knowledge_content,
                'word_count': len(knowledge_content.split()),
                'char_count': len(knowledge_content)
            }], f, indent=2, ensure_ascii=False)

    # Save formatted content
    with open("swiftfixpro_knowledge.txt", 'w', encoding='utf-8') as f:
        f.write(knowledge_content)

    print("\n📄 Formatted knowledge saved to swiftfixpro_knowledge.txt")
    print(f"📊 Total content: {len(knowledge_content)} characters")

    return knowledge_content

if __name__ == "__main__":
    main()