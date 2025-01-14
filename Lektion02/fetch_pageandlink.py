from urllib.parse import urljoin

from bs4 import BeautifulSoup, Comment 
import requests

def fetch_html(url):
    """Fetches HTML content of a URL and returns visible text in the browser."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove elements that typically don't contain visible text
        for element in soup(['script', 'style', 'meta', 'head', 'footer', 'link', 'noscript']):
            element.extract()

        # Remove comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # Get visible text
        visible_text = soup.get_text(separator=' ', strip=True)
        return soup, visible_text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None, None

def extract_links(soup, base_url):
    """Extracts and returns all unique links from a BeautifulSoup object."""
    links = set()
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        full_url = urljoin(base_url, href)
        links.add(full_url)
    return links