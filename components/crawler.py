
from bs4 import BeautifulSoup
import requests
from time import sleep
from urllib.parse import urljoin
from components.robots_processor import RobotsProcessor
from components.near_duplicate import Jaccard
from components.logger import Logger
SIMILARITY_THRESHOLD : float = 0.90

class Crawler:
    def __init__(self, pages_size, seed_url):
        self.pages_size = pages_size
        self.seed_url = seed_url
        self.visited = set()  # To track visited URLs
        self.to_visit = [seed_url]  # Seed URL to start with
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
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        
        return soup

    
    def crawl(self):
        """Main function to start crawling."""
        logger = Logger()
        while self.to_visit and len(self.pages) < self.pages_size:
            current_url = self.to_visit.pop(0)

            # Check if we are allowed to crawl this URL
            if not self.robots_processor.can_fetch(current_url):
                continue

            if current_url not in self.visited:
                logger.time(f"Crawling: {current_url}")
                html_content = self.fetch_page(current_url)

                if html_content:
                    clean_html = self.clean_html(html_content)
                    jaccard = Jaccard()
                    if jaccard.near_duplicate(str(clean_html),self.pages, SIMILARITY_THRESHOLD):
                        continue
                    self.pages[current_url] = str(clean_html)  # Store cleaned HTML
                    self.visited.add(current_url)

                    # Find new URLs to crawl from cleaned HTML
                    self.add_new_links(clean_html, current_url)

                # Politeness (1-second delay between requests)
                logger.endtime(f"Crawling: {current_url}")
                sleep(1)

        print(f"Crawling complete. {len(self.pages)} pages stored.")
        return self.pages  # Return the stored pages

    def add_new_links(self, clean_html, base_url):
        """Extract and add new links from the cleaned HTML."""
        for link in clean_html.find_all('a', href=True):
            new_url = urljoin(base_url, link['href'])
            if new_url not in self.visited and new_url not in self.to_visit:
                self.to_visit.append(new_url)

