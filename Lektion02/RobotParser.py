from urllib.parse import urlparse, urlunparse

import requests

from .FindCrawlDelay import find_crawl_delay
from .FindUserAgents import find_user_agents
from .ParseRules import parse_rules


def Robotparser(url, user_agent="*"):
    """Main function to parse robots.txt from a URL and return rules, crawl-delay, and sitemaps."""
    
    # Parse the URL to get the base URL
    parsed_url = urlparse(url)
    
    # Construct the base URL (scheme and netloc) and append /robots.txt
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
    robots_txt_url = f"{base_url}/robots.txt"
    
    try:
        # Fetch the robots.txt content from the constructed URL
        print(f"\'{robots_txt_url}\'")
        response = requests.Session().get(robots_txt_url)
        response.raise_for_status()  # Raise an error for bad responses (e.g., 404)
        robots_txt_content = response.text
    except requests.RequestException as e:
        print(f"Error fetching robots.txt from {robots_txt_url}: {e}")
        return None
    
    # Step 1: Find user-agent sections
    user_agent_sections = find_user_agents(robots_txt_content, user_agent)

    # Step 2: Extract Allow and Disallow rules
    rules = parse_rules(user_agent_sections)

    # Step 3: Extract Crawl-delay, if present
    crawl_delay = find_crawl_delay(user_agent_sections)

    return {
        "Disallow": rules["Disallow"],  # Only returning Disallow rules
        "Crawl-delay": crawl_delay, 
    }
