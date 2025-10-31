#!/usr/bin/env python3
"""
JavaScript-Enabled Web Scraper for SwiftFixPro
Uses Selenium to render JavaScript and extract actual content.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from typing import Dict, List

class JSEnabledScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.scraped_content = []

    def setup_driver(self):
        """Setup Chrome WebDriver with options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize WebDriver: {e}")
            raise

    def wait_for_content(self, timeout=10):
        """Wait for page content to load."""
        try:
            # Wait for body to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            # Wait a bit more for dynamic content
            time.sleep(3)
            print("✅ Page content loaded")
        except Exception as e:
            print(f"⚠️ Timeout waiting for content: {e}")

    def expand_faq_accordions(self):
        """Expand all FAQ accordion sections to reveal hidden content."""
        try:
            print("🔍 Expanding FAQ accordions...")
            
            # Wait for accordion elements to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".border-gray-200"))
            )
            
            # Find all accordion buttons
            accordion_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.w-full.p-4.text-left")
            
            print(f"Found {len(accordion_buttons)} accordion buttons")
            
            # Try to expand each accordion by simulating the click and waiting for content
            for i, button in enumerate(accordion_buttons):
                try:
                    # Scroll to button
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                    
                    # Get button text for logging
                    button_text = button.find_element(By.CSS_SELECTOR, "span").text.strip()[:50]
                    
                    # Check if accordion is already expanded (has content visible)
                    parent_div = button.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
                    content_divs = parent_div.find_elements(By.CSS_SELECTOR, ".overflow-hidden .p-4.pt-0")
                    
                    if content_divs and any(div.is_displayed() for div in content_divs):
                        print(f"✅ Accordion {i+1} already expanded: {button_text}")
                        continue
                    
                    # Try multiple click methods
                    try:
                        # Method 1: Direct click
                        button.click()
                        print(f"🖱️ Clicked accordion {i+1} (direct): {button_text}")
                    except:
                        try:
                            # Method 2: JavaScript click
                            self.driver.execute_script("arguments[0].click();", button)
                            print(f"🖱️ Clicked accordion {i+1} (JS): {button_text}")
                        except:
                            print(f"⚠️ Could not click accordion {i+1}: {button_text}")
                            continue
                    
                    # Wait for content to appear
                    time.sleep(3)
                    
                    # Check if content appeared
                    content_divs = parent_div.find_elements(By.CSS_SELECTOR, ".overflow-hidden .p-4.pt-0")
                    if content_divs:
                        for div in content_divs:
                            if div.is_displayed():
                                content_text = div.text.strip()
                                if content_text:
                                    print(f"📄 Content appeared for accordion {i+1}: {content_text[:100]}...")
                                    break
                    
                except Exception as e:
                    print(f"⚠️ Error processing accordion {i+1}: {e}")
                    continue
            
            # Additional wait for all content to load
            time.sleep(5)
            
            # Debug: Save page source after expansion
            if '/faq' in self.driver.current_url:
                with open("faq_page_source_after_clicks.html", 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
                print("💾 Saved FAQ page source after clicks for debugging")
            
            print("✅ FAQ accordions expansion attempt completed")
            
        except Exception as e:
            print(f"⚠️ Error expanding FAQ accordions: {e}")

    def extract_page_content(self, url: str) -> Dict:
        """Extract content from a single page using JavaScript rendering."""
        try:
            print(f"🌐 Loading: {url}")
            self.driver.get(url)

            # Wait for content to load
            self.wait_for_content()

            # Special handling for FAQ page - expand accordions
            if '/faq' in url:
                self.expand_faq_accordions()

            # Extract various content elements
            content_data = {
                'url': url,
                'title': self.driver.title,
                'meta_description': '',
                'content': '',
                'headings': [],
                'paragraphs': [],
                'links': []
            }

            # Get meta description
            try:
                meta_desc = self.driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]')
                content_data['meta_description'] = meta_desc.get_attribute('content') or ''
            except:
                pass

            # Get all headings
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                try:
                    headings = self.driver.find_elements(By.TAG_NAME, tag)
                    for h in headings:
                        text = h.text.strip()
                        if text:
                            content_data['headings'].append(f"{tag.upper()}: {text}")
                except:
                    pass

            # Get all paragraphs
            try:
                paragraphs = self.driver.find_elements(By.TAG_NAME, 'p')
                for p in paragraphs:
                    text = p.text.strip()
                    if text and len(text) > 10:  # Filter out very short text
                        content_data['paragraphs'].append(text)
            except:
                pass

            # Special extraction for FAQ accordion content
            if '/faq' in url:
                try:
                    # Find all expanded accordion content areas
                    accordion_contents = self.driver.find_elements(By.CSS_SELECTOR, ".overflow-hidden .p-4.pt-0")
                    faq_answers = []
                    
                    for content_div in accordion_contents:
                        try:
                            # Check if the content is visible
                            if content_div.is_displayed():
                                text = content_div.text.strip()
                                if text and len(text) > 20:  # Substantial content
                                    faq_answers.append(text)
                                    print(f"📝 Extracted FAQ content: {text[:100]}...")
                        except:
                            continue
                    
                    # Also try to find any visible content that might be dynamically loaded
                    try:
                        # Look for any div with substantial text content that might be FAQ answers
                        all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                        for div in all_divs:
                            try:
                                if div.is_displayed():
                                    text = div.text.strip()
                                    # Look for content that looks like FAQ answers (longer paragraphs)
                                    if (text and len(text) > 100 and 
                                        not any(skip in text.lower() for skip in ['cookie', 'privacy', 'subscribe', 'footer', 'header', 'nav']) and
                                        any(keyword in text.lower() for keyword in ['swift fix pro', 'singapore', 'service', 'maintenance', 'property'])):
                                        if text not in faq_answers:
                                            faq_answers.append(text)
                                            print(f"📝 Found additional FAQ content: {text[:100]}...")
                            except:
                                continue
                    except:
                        pass
                    
                    # Add found answers to paragraphs
                    for answer in faq_answers:
                        content_data['paragraphs'].append(f"FAQ Answer: {answer}")
                    
                    print(f"📋 Found {len(faq_answers)} FAQ answers total")
                    
                except Exception as e:
                    print(f"⚠️ Error extracting FAQ accordion content: {e}")

            # Get all links
            try:
                links = self.driver.find_elements(By.TAG_NAME, 'a')
                for link in links:
                    href = link.get_attribute('href')
                    text = link.text.strip()
                    if href and text and len(text) > 3:
                        content_data['links'].append(f"{text}: {href}")
            except:
                pass

            # Get main content area (try common selectors)
            content_selectors = [
                'main', '.content', '.main-content', '#content',
                '.page-content', '.entry-content', 'article',
                '.site-content', '#main', '.container'
            ]

            main_content = ""
            for selector in content_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        if text and len(text) > main_content:
                            main_content = text
                except:
                    continue

            # For FAQ page, also include expanded accordion content
            if '/faq' in url:
                try:
                    accordion_texts = []
                    accordion_contents = self.driver.find_elements(By.CSS_SELECTOR, ".overflow-hidden .p-4.pt-0.border-t")
                    for content_div in accordion_contents:
                        text = content_div.text.strip()
                        if text and len(text) > 20:
                            accordion_texts.append(text)
                    
                    if accordion_texts:
                        main_content += "\n\n--- FAQ ANSWERS ---\n\n" + "\n\n".join(accordion_texts)
                        print(f"📋 Added {len(accordion_texts)} FAQ answers to main content")
                except Exception as e:
                    print(f"⚠️ Error adding FAQ content to main content: {e}")

            # If no main content found, get all body text
            if not main_content:
                try:
                    body = self.driver.find_element(By.TAG_NAME, 'body')
                    main_content = body.text.strip()
                except:
                    main_content = "Unable to extract content"

            content_data['content'] = main_content

            # Calculate stats
            content_data['word_count'] = len(main_content.split())
            content_data['char_count'] = len(main_content)
            content_data['heading_count'] = len(content_data['headings'])
            content_data['paragraph_count'] = len(content_data['paragraphs'])
            content_data['link_count'] = len(content_data['links'])

            print(f"📊 Extracted: {content_data['word_count']} words, {content_data['heading_count']} headings, {content_data['paragraph_count']} paragraphs")

            return content_data

        except Exception as e:
            print(f"❌ Error extracting content from {url}: {e}")
            return {
                'url': url,
                'title': 'Error',
                'content': f"Failed to extract content: {str(e)}",
                'word_count': 0,
                'char_count': 0,
                'headings': [],
                'paragraphs': [],
                'links': []
            }

    def scrape_subpages(self, base_url: str, subpages: List[str] = None) -> List[Dict]:
        """Scrape multiple subpages from a website."""
        if subpages is None:
            subpages = [
                '', '/about', '/services', '/products', '/contact',
                '/faq', '/pricing', '/blog', '/news', '/support', '/docs'
            ]

        print(f"🚀 Starting JavaScript-enabled scraping of {len(subpages)} pages from {base_url}")
        print("=" * 70)

        # Setup driver
        self.setup_driver()

        try:
            for subpage in subpages:
                url = f"{base_url.rstrip('/')}{subpage}" if subpage else base_url

                content = self.extract_page_content(url)

                if content['char_count'] > 50:  # Only save substantial content
                    self.scraped_content.append(content)
                    print(f"✅ Saved page: {content['title'][:50]}... ({content['word_count']} words)")
                else:
                    print(f"⚠️ Skipped page (too little content): {content['title'][:30]}...")

                time.sleep(2)  # Be respectful

        finally:
            if self.driver:
                self.driver.quit()
                print("🛑 WebDriver closed")

        return self.scraped_content

    def save_to_json(self, filename: str = "swiftfixpro_js_content.json"):
        """Save scraped content to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_content, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(self.scraped_content)} pages to {filename}")

    def format_for_knowledge_base(self) -> str:
        """Format scraped content for addition to knowledge base."""
        formatted_content = []

        for page in self.scraped_content:
            page_content = f"""
# {page['title']}

URL: {page['url']}

{page['meta_description']}

## Headings:
{chr(10).join(page['headings'])}

## Content:
{page['content']}

## Key Information:
- Word Count: {page['word_count']}
- Headings: {page['heading_count']}
- Paragraphs: {page['paragraph_count']}
- Links: {page['link_count']}
"""
            formatted_content.append(page_content.strip())

        return "\n\n---\n\n".join(formatted_content)

def main():
    """Main scraping function with JavaScript support."""
    import sys

    # Get URL from command line argument or use default
    if len(sys.argv) > 1:
        website_url = sys.argv[1]
    else:
        website_url = "https://www.swiftfixpro.com"

    print(f"🌐 JavaScript-Enabled Scraper for: {website_url}")
    print("This will open a headless Chrome browser to render the website content...")

    # Scrape with JavaScript support
    scraper = JSEnabledScraper(headless=True)  # Set to False to see browser window
    scraped_pages = scraper.scrape_subpages(website_url)

    if scraped_pages:
        print(f"\n🎉 Successfully scraped {len(scraped_pages)} pages with JavaScript rendering!")

        # Save raw data
        scraper.save_to_json()

        # Format for knowledge base
        knowledge_content = scraper.format_for_knowledge_base()
    else:
        print("\n❌ No content was scraped successfully.")
        knowledge_content = "No content extracted from website."

    # Save formatted content
    with open("swiftfixpro_js_knowledge.txt", 'w', encoding='utf-8') as f:
        f.write(knowledge_content)

    print("\n📄 Formatted knowledge saved to swiftfixpro_js_knowledge.txt")
    print(f"📊 Total content: {len(knowledge_content)} characters")

    # Show summary
    total_words = sum(page['word_count'] for page in scraped_pages)
    total_headings = sum(page['heading_count'] for page in scraped_pages)
    print(f"📈 Summary: {len(scraped_pages)} pages, {total_words} words, {total_headings} headings")

    return knowledge_content

if __name__ == "__main__":
    main()