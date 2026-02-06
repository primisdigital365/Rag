from playwright.sync_api import sync_playwright
import time

def fetch_rendered_text(url: str, scroll_times: int = 10) -> str:
    """
    Fetch fully rendered text from a dynamic website
    
    Args:
        url: URL to scrape
        scroll_times: Number of times to scroll down (for lazy loading)
    
    Returns:
        Rendered text content
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to page
            page.goto(url, timeout=60000)

            # Wait for initial content to load
            page.wait_for_load_state("networkidle")

            # Auto-scroll to bottom to trigger lazy loading
            previous_height = 0
            for _ in range(scroll_times):
                current_height = page.evaluate("document.body.scrollHeight")
                if current_height == previous_height:
                    break
                previous_height = current_height
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            # Extract text AFTER scrolling
            text = page.evaluate("document.body.innerText")

            browser.close()
            return text
            
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            browser.close()
            return ""


def fetch_rendered_html(url: str, scroll_times: int = 10) -> str:
    """
    Fetch fully rendered HTML from a dynamic website
    
    Args:
        url: URL to scrape
        scroll_times: Number of times to scroll down
    
    Returns:
        Rendered HTML content
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")

            # Scroll to load all content
            for _ in range(scroll_times):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)

            # Get HTML
            html = page.content()

            browser.close()
            return html
            
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            browser.close()
            return ""


def fetch_with_wait_for_selector(url: str, selector: str, timeout: int = 30000) -> str:
    """
    Fetch page content after waiting for a specific selector
    Useful when you know content loads in a specific element
    
    Args:
        url: URL to scrape
        selector: CSS selector to wait for
        timeout: Maximum time to wait in milliseconds
    
    Returns:
        Rendered text content
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)
            
            # Wait for specific selector
            page.wait_for_selector(selector, timeout=timeout)
            
            # Additional wait for any lazy loading
            time.sleep(2)
            
            # Scroll through page
            for i in range(5):
                page.evaluate(f"window.scrollTo(0, {i * 1000})")
                time.sleep(0.5)
            
            text = page.evaluate("document.body.innerText")
            
            browser.close()
            return text
            
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            browser.close()
            return ""


def extract_links(url: str) -> list:
    """
    Extract all links from a page
    
    Args:
        url: URL to scrape
    
    Returns:
        List of URLs found on the page
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            
            # Extract all href attributes
            links = page.evaluate("""
                () => {
                    const anchors = Array.from(document.querySelectorAll('a[href]'));
                    return anchors.map(a => a.href).filter(href => href);
                }
            """)
            
            browser.close()
            return links
            
        except Exception as e:
            print(f"❌ Error extracting links from {url}: {e}")
            browser.close()
            return []


def extract_structured_content(url: str) -> dict:
    """
    Extract structured content from a page
    
    Args:
        url: URL to scrape
    
    Returns:
        Dictionary with title, headings, paragraphs, and links
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            
            # Wait and scroll
            time.sleep(2)
            for i in range(5):
                page.evaluate(f"window.scrollTo(0, {i * 1000})")
                time.sleep(0.5)
            
            # Extract structured data
            data = page.evaluate("""
                () => {
                    return {
                        title: document.title,
                        h1: Array.from(document.querySelectorAll('h1')).map(h => h.innerText),
                        h2: Array.from(document.querySelectorAll('h2')).map(h => h.innerText),
                        h3: Array.from(document.querySelectorAll('h3')).map(h => h.innerText),
                        paragraphs: Array.from(document.querySelectorAll('p')).map(p => p.innerText).filter(t => t.length > 20),
                        links: Array.from(document.querySelectorAll('a[href]')).map(a => ({
                            text: a.innerText,
                            href: a.href
                        })),
                        meta_description: document.querySelector('meta[name="description"]')?.content || ''
                    };
                }
            """)
            
            browser.close()
            return data
            
        except Exception as e:
            print(f"❌ Error extracting structured content from {url}: {e}")
            browser.close()
            return {}


def test_playwright():
    """Test if Playwright is working correctly"""
    test_url = "https://example.com"
    
    print(f"🧪 Testing Playwright with {test_url}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(test_url)
            title = page.title()
            browser.close()
            
            print(f"✅ Success! Page title: {title}")
            return True
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        print("\n💡 Make sure you've installed Playwright browsers:")
        print("   playwright install chromium")
        return False


if __name__ == "__main__":
    # Test Playwright installation
    if test_playwright():
        print("\n✅ Playwright is working correctly!")
        
        # Test with a real URL
        print("\n🧪 Testing with primisdigital.com...")
        text = fetch_rendered_text("https://primisdigital.com")
        
        if text:
            print(f"✅ Successfully fetched content ({len(text)} characters)")
            print(f"\nPreview:\n{text[:500]}...")
        else:
            print("❌ Failed to fetch content")
    else:
        print("\n❌ Playwright is not working. Please install it:")
        print("   pip install playwright")
        print("   playwright install chromium")