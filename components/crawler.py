
from bs4 import BeautifulSoup
import requests
from time import sleep, time
from urllib.parse import urljoin, urlparse
from components.robots_processor import RobotsProcessor
from components.near_duplicate import Jaccard
from components.logger import Logger

SIMILARITY_THRESHOLD: float = 0.90

class Crawler:
    def __init__(self, pages_size, seed_urls):
        self.pages_size = pages_size
        self.seed_url = seed_urls if isinstance(seed_urls, list) else [seed_urls]  # Ensure seed_url is a list
        self.visited = set()  # To track visited URLs
        self.to_visit = self.seed_url.copy()  # Seed URL to start with
        self.pages = {}  # To store {url: html_content}
        self.robots_processor = RobotsProcessor()

    def fetch_page(self, url):
        """Fetch the HTML content of a given URL."""
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def clean_html(self, html_content):
        """Remove <script> and <style> tags from the HTML."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove <script> and <style> tags
        for element in soup(['script', 'style', 'meta', 'head', 'footer', 'link', 'noscript']):
            element.extract()

        return soup

    def crawl(self):
        """Main function to start crawling."""
        logger = Logger()
        current_hostname = urlparse(self.to_visit[0]).hostname
        
        while self.to_visit and len(self.pages) < self.pages_size:
            current_url = self.to_visit.pop(0)
            current_hostname = urlparse(current_url).hostname

            # Check if we are allowed to crawl this URL
            if not self.robots_processor.can_fetch(current_url):
                continue

            if current_url not in self.visited:
                logger.time(f"Crawl: {current_url}")
                logger.time(f"Fetch: {current_url}")
                html_content = self.fetch_page(current_url)
                logger.endtime(f"Fetch: {current_url}")

                startTime = time() 

                if html_content:
                    clean_html = self.clean_html(html_content)
                    jaccard = Jaccard()
                    if jaccard.near_duplicate(str(clean_html), self.pages, SIMILARITY_THRESHOLD):
                        continue
                    self.pages[current_url] = str(clean_html)  # Store cleaned HTML
                    self.visited.add(current_url)

                    # Find new URLs to crawl from cleaned HTML
                    self.add_new_links(clean_html, current_url)

                logger.endtime(f"Crawl: {current_url}")
                print('\n')
                endTime = time()
                duration = endTime - startTime
                # Check if the next URL has a different hostname
                if self.to_visit:
                    next_url = self.to_visit[0]
                    next_hostname = urlparse(next_url).hostname
                    if next_hostname != current_hostname:
                        # Skip sleep for different hostname
                        sleep(0)
                    elif duration > 1:
                        sleep(0)
                    else:
                        # Politeness (1-second delay between requests)
                        sleep(1)

                
        print(f"Crawling complete. {len(self.pages)} pages stored.")
        return self.pages  # Return the stored pages


    def normalize_url(self, url):
        """Normalize the URL by removing 'www.' if it exists."""
        parsed_url = urlparse(url)
        if parsed_url.hostname.startswith("www."):
            normalized_hostname = parsed_url.hostname[4:]  # Remove 'www.'
            normalized_url = urljoin(url, parsed_url._replace(netloc=normalized_hostname).geturl())
            return normalized_url
        return url

    def add_new_links(self, clean_html, base_url):
        """Extract and add new links from the cleaned HTML."""
        for link in clean_html.find_all('a', href=True):
            new_url = urljoin(base_url, link['href'])

            # Check if the new URL is a valid web link (http or https)
            if new_url.startswith(('http://', 'https://')):
                normalized_new_url = self.normalize_url(new_url)
                normalized_base_url = self.normalize_url(base_url)

                # Skip in-links based on ignored paths and check against normalized URLs
                if normalized_new_url != normalized_base_url and normalized_new_url not in self.visited and normalized_new_url not in self.to_visit:
                    self.to_visit.append(new_url)


