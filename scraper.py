import requests
from bs4 import BeautifulSoup
import time
import os
import json
import logging
import redis
import hashlib
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, InvalidSessionIdException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CDPScraper:
    def __init__(self, output_dir="scraped_data", use_redis=True, redis_host='localhost', redis_port=6379, redis_db=0, redis_ttl=86400):
        self.output_dir = output_dir
        self.visited_urls = set()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # Redis configuration
        self.use_redis = use_redis
        if use_redis:
            try:
                self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
                self.redis_ttl = redis_ttl  # Cache TTL in seconds (default: 1 day)
                logging.info("Redis cache initialized")
            except redis.ConnectionError:
                logging.warning("Failed to connect to Redis. Running without cache.")
                self.use_redis = False
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Selenium configuration
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--enable-javascript")
        self.chrome_options.add_argument("--window-size=1920,1080")  # Larger viewport
        self.chrome_options.add_argument("--disable-gpu")  # Helps avoid crashes
        self.chrome_options.add_argument("--disable-web-security")  # May help with some sites
        self.init_webdriver()
        
        # Tracking scraping metrics
        self.pages_visited = 0
        self.driver_resets = 0
        
        # Platform-specific configurations
        self.platform_configs = {
            "segment": {
                "selectors": [".docs-content", "article", ".main-content", ".content", "main"],
                "doc_terms": ['docs', 'guide', 'tutorial', 'how-to']
            },
            "mparticle": {
                "selectors": [".doc-content", ".main-content", "article", "main"],
                "doc_terms": ['docs', 'guide', 'tutorial', 'how-to']
            },
            "lytics": {
                "selectors": [".main-content", ".documentation-content", "article", "main"],
                "doc_terms": ['docs', 'guide', 'tutorial', 'how-to']
            },
            "zeotap": {
                "selectors": ["#html", ".main", ".page-content", "div[role='main']", ".docs-content", 
                             ".documentation", ".doc-content", "#root", "body"],
                "doc_terms": ['docs', 'guide', 'tutorial', 'how-to', 'implementation', 'integration']
            }
        }
    
    def init_webdriver(self):
        """Initialize or reinitialize the WebDriver"""
        try:
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except Exception as e:
                    logging.warning(f"Error closing existing WebDriver: {str(e)}")
        except Exception:
            pass
            
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.set_page_load_timeout(30)  # Set page load timeout
            logging.info("WebDriver initialized")
        except Exception as e:
            logging.error(f"Error initializing WebDriver: {str(e)}")
            raise
    
    def reset_driver(self):
        """Reset WebDriver when issues occur"""
        self.init_webdriver()
        self.driver_resets += 1
        logging.info(f"WebDriver has been reset (total resets: {self.driver_resets})")
        time.sleep(2)  # Give the driver a moment after reset
    
    def _get_cache_key(self, url):
        """Generate a unique cache key for the URL"""
        return f"cdpscraper:{hashlib.md5(url.encode()).hexdigest()}"
    
    def _get_from_cache(self, url):
        """Retrieve data from Redis cache if available"""
        if not self.use_redis:
            return None
        
        try:
            cache_key = self._get_cache_key(url)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logging.info(f"Cache hit for {url}")
                return json.loads(cached_data)
        except Exception as e:
            logging.warning(f"Error retrieving from cache: {str(e)}")
        
        return None
    
    def _save_to_cache(self, url, data):
        """Save data to Redis cache"""
        if not self.use_redis or not data:
            return
        
        try:
            cache_key = self._get_cache_key(url)
            self.redis_client.setex(
                cache_key,
                self.redis_ttl,
                json.dumps(data)
            )
            logging.info(f"Saved to cache: {url}")
        except Exception as e:
            logging.warning(f"Error saving to cache: {str(e)}")
    
    def _safe_selenium_operation(self, operation, url, *args, max_retries=2, **kwargs):
        """Safely execute a Selenium operation with retries"""
        retry_count = 0
        while retry_count <= max_retries:
            try:
                return operation(*args, **kwargs)
            except (WebDriverException, InvalidSessionIdException) as e:
                retry_count += 1
                logging.warning(f"Selenium error (attempt {retry_count}/{max_retries+1}) on {url}: {str(e)}")
                
                if retry_count <= max_retries:
                    logging.info(f"Resetting driver and retrying...")
                    self.reset_driver()
                    time.sleep(2 * retry_count)  # Exponential backoff
                else:
                    logging.error(f"Failed after {max_retries+1} attempts: {url}")
                    raise
    
    def _scrape_with_selenium(self, url, selectors):
        """Scrape content using Selenium for dynamic pages with better error handling"""
        def _perform_scrape():
            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
            time.sleep(5)  # Wait for React rendering
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            for selector in selectors if isinstance(selectors, list) else [selectors]:
                elements = soup.select(selector)
                if elements:
                    return elements, soup
            
            body = soup.find('body')
            return [body] if body else [], soup
        
        try:
            elements, soup = self._safe_selenium_operation(_perform_scrape, url)
            return elements, soup
        except Exception as e:
            logging.error(f"Selenium scraping failed for {url}: {str(e)}")
            return [], None
    
    def _extract_links_selenium(self, url, doc_terms):
        """Extract links using Selenium with better error handling"""
        def _perform_link_extraction():
            self.driver.get(url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
            time.sleep(3)  # Wait for React to render
            
            links = []
            for a in self.driver.find_elements(By.TAG_NAME, "a"):
                try:
                    href = a.get_attribute("href")
                    if href and any(term in href.lower() for term in doc_terms):
                        links.append(href)
                except:
                    continue
            return links
        
        try:
            return self._safe_selenium_operation(_perform_link_extraction, url)
        except Exception as e:
            logging.error(f"Error extracting links with Selenium: {str(e)}")
            return []
    
    def scrape_url(self, url, platform_name=None, max_pages=100, wait_time=1, depth=0):
        """Scrape content from URL with improved handling for React-based sites and recursion protection"""
        # Prevent excessive recursion
        max_depth = 5
        if depth >= max_depth:
            logging.info(f"Max depth reached at {url}")
            return []
            
        # Prevent excessive pages
        if url in self.visited_urls or len(self.visited_urls) >= max_pages:
            return []
        
        self.visited_urls.add(url)
        self.pages_visited += 1
        logging.info(f"Scraping: {url} (depth: {depth}, pages visited: {self.pages_visited})")
        
        # Check cache first
        cached_data = self._get_from_cache(url)
        if cached_data:
            return cached_data
        
        # Auto-reset driver after certain number of pages to prevent memory issues
        if self.pages_visited % 20 == 0:
            logging.info("Performing routine WebDriver reset")
            self.reset_driver()
        
        try:
            content_elements = []
            soup = None
            
            # For zeotap or at deeper levels, go directly to Selenium as it's likely a React app
            if platform_name == "zeotap" or depth > 2:
                selectors = self.platform_configs.get(platform_name, {}).get("selectors", [])
                content_elements, soup = self._scrape_with_selenium(url, selectors)
            else:
                # Original code for other platforms
                try:
                    response = self.session.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    selectors = self.platform_configs.get(platform_name, {}).get("selectors", ["article", ".main-content", ".content", "main"])
                    
                    for selector in selectors:
                        content_elements = soup.select(selector)
                        if content_elements:
                            break
                    
                    if not content_elements:
                        logging.warning(f"No content found with selectors {selectors}. Trying Selenium.")
                        content_elements, soup = self._scrape_with_selenium(url, selectors)
                except requests.exceptions.RequestException as e:
                    logging.warning(f"Request failed for {url}: {str(e)}. Trying Selenium.")
                    content_elements, soup = self._scrape_with_selenium(url, selectors)
            
            # If still no content or soup, return empty
            if not content_elements or not soup:
                logging.warning(f"No content found on {url}.")
                return []
            
            scraped_data = []
            for element in content_elements:
                text_content = element.get_text(separator='\n', strip=True)
                
                if not self._is_relevant_content(text_content):
                    continue  
                
                # Additional metadata extraction
                metadata = self._extract_metadata(soup, url, platform_name)
                
                scraped_data.append({
                    "url": url,
                    "title": metadata["title"],
                    "platform": platform_name,
                    "category": metadata["category"],
                    "content": text_content,
                    "html": str(element)
                })
            
            # Save current data to cache before recursing
            self._save_to_cache(url, scraped_data)
            
            # Process discovered links with recursion limiter
            if depth < max_depth - 1:  # Only process links if not at max_depth-1
                domain = urlparse(url).netloc
                links_to_scrape = []
                
                if platform_name == "zeotap":
                    doc_terms = self.platform_configs.get(platform_name, {}).get("doc_terms", ['docs', 'how', 'guide'])
                    links_to_scrape = self._extract_links_selenium(url, doc_terms)
                    # Filter links to keep only domain-specific ones and not already visited
                    links_to_scrape = [link for link in links_to_scrape 
                                     if urlparse(link).netloc == domain and link not in self.visited_urls]
                else:
                    # Original link extraction code
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag['href']
                        full_url = urljoin(url, href)
                        
                        if urlparse(full_url).netloc == domain and full_url not in self.visited_urls:
                            doc_terms = self.platform_configs.get(platform_name, {}).get("doc_terms", ['docs', 'how', 'guide'])
                            if self._is_documentation_link(full_url, href, doc_terms):
                                links_to_scrape.append(full_url)
                
                # Limit number of links to scrape at each level to prevent explosion
                max_links_per_level = 10
                links_to_scrape = links_to_scrape[:max_links_per_level]
                
                for link in links_to_scrape:
                    time.sleep(wait_time)
                    additional_data = self.scrape_url(link, platform_name, max_pages, wait_time, depth+1)
                    scraped_data.extend(additional_data)
            
            return scraped_data
        
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            # If we get a Selenium error, reset the driver
            if isinstance(e, (WebDriverException, InvalidSessionIdException)):
                self.reset_driver()
            return []
    
    def _extract_metadata(self, soup, url, platform_name):
        """Extract additional metadata from the page"""
        metadata = {
            "title": self._extract_title(soup),
            "category": self._extract_category_from_url(url)
        }
        
        # Extract breadcrumbs if available
        breadcrumbs = soup.select(".breadcrumbs, .breadcrumb, .doc-breadcrumb")
        if breadcrumbs:
            crumbs = [b.get_text(strip=True) for b in breadcrumbs[0].find_all("li")]
            if crumbs and not metadata["category"]:
                metadata["category"] = " > ".join(crumbs)
        
        return metadata
    
    def _extract_title(self, soup):
        """Extract page title"""
        # Try specific heading elements first
        for selector in ['h1.document-title', 'h1.page-title', '.document-title h1', 'main h1', 'h1']:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text(strip=True)
        
        # Fallback to regular title tag
        return soup.find('title').get_text(strip=True) if soup.find('title') else "No title found"
    
    def _extract_category_from_url(self, url):
        """Extract category from URL path"""
        path = urlparse(url).path.strip('/')
        parts = path.split('/')
        
        if len(parts) > 1:
            return parts[0].replace('-', ' ').title()
        return "General"
    
    def _is_documentation_link(self, full_url, href, doc_terms=None):
        """Check if URL is likely a documentation page"""
        if doc_terms is None:
            doc_terms = ['docs', 'how', 'guide', 'tutorial', 'setup', 'faq', 'best-practices']
            
        exclude_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.js', '.css', '.xml', '.ico']
        exclude_keywords = ['login', 'signup', 'signin', 'register', 'twitter', 'facebook', 'linkedin', 'community', '#']
        
        return not any(full_url.lower().endswith(ext) for ext in exclude_extensions) and \
               not any(skip in href.lower() for skip in exclude_keywords) and \
               any(term in full_url.lower() for term in doc_terms)
    
    def _is_relevant_content(self, text):
        """Check if content is a relevant how-to guide"""
        if not text or len(text) < 50:  # Skip very short content
            return False
            
        relevant_phrases = [
            'how to', 'steps to', 'set up', 'setup', 'configure', 'tutorial', 
            'walkthrough', 'best practices', 'implementation', 'integrate', 
            'integration', 'guide', 'instructions'
        ]
        
        return any(phrase in text.lower() for phrase in relevant_phrases)
    
    def save_data(self, data, platform_name):
        """Save scraped data to JSON file"""
        filename = os.path.join(self.output_dir, f"{platform_name}_howto.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Saved {len(data)} guides to {filename}")
    
    def scrape_cdp_guides(self):
        """Main method to scrape all CDP platforms"""
        sources = {
            "segment": "https://segment.com/docs/?ref=nav",
            "mparticle": "https://docs.mparticle.com/",
            "lytics": "https://docs.lytics.com/",
            "zeotap": "https://docs.zeotap.com/home/en-us/"
        }
        
        all_data = {}
        
        for platform, url in sources.items():
            try:
                logging.info(f"Starting scrape of {platform} guides...")
                data = self.scrape_url(url, platform_name=platform, max_pages=200)
                self.save_data(data, platform)
                all_data[platform] = data
                
                logging.info(f"Completed {platform} scrape. Pages visited: {self.pages_visited}, driver resets: {self.driver_resets}")
                
                # Reset counters and visited URLs between platforms
                self.visited_urls.clear()
                self.pages_visited = 0
                self.driver_resets = 0
                
                # Always reset driver between platforms
                self.reset_driver()
                time.sleep(5)  # Longer pause between platforms
                
            except Exception as e:
                logging.error(f"Failed to scrape {platform}: {str(e)}")
                continue
        
        # Save a consolidated file with all platforms
        consolidated_file = os.path.join(self.output_dir, "all_cdp_guides.json")
        with open(consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        logging.info("Scraping Complete.")
        
        try:
            self.driver.quit()  # Close the Selenium driver
        except:
            pass  # Ignore errors during final quit

# Example usage
if __name__ == "__main__":
    try:
        scraper = CDPScraper(
            output_dir="cdp_data",
            use_redis=True,
        )
        scraper.scrape_cdp_guides()
    except Exception as e:
        logging.critical(f"Critical error in scraper: {str(e)}")
        # Try to clean up WebDriver if possible
        try:
            if hasattr(scraper, 'driver') and scraper.driver:
                scraper.driver.quit()
        except:
            pass