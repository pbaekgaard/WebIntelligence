import asyncio
import json
from urllib.parse import urlparse

from tldextract import extract

from .DocFPs import store_in_dict
from .DuplicateURL import duplicateUrl
from .fetch_pageandlink import extract_links, fetch_html
from .RobotParser import Robotparser
from .url_filter import url_filter

URL_seed = [
    "https://www.insuremytrip.com/",
    "https://www.dr.dk/",
]

URL_frontier = []

import json
import random
import time
from collections import deque
from urllib.parse import urlparse


def get_base_domain(url):
    """Extract base domain from URL."""
    extracted = extract(url)
    return extracted.domain + '.' + extracted.suffix

def find_different_domain_url(frontier, current_domain):
    """Find next URL with different base domain in frontier."""
    # Create list of indices with different domains
    different_domains = []
    for i, url in enumerate(frontier):
        if get_base_domain(url) != current_domain:
            different_domains.append(i)
    
    if different_domains:
        idx = random.choice(different_domains)
        # Convert to list once for the removal
        frontier_list = list(frontier)
        found_url = frontier_list.pop(idx)
        frontier.clear()
        frontier.extend(frontier_list)
        return found_url
    return None

async def start_crawler(URLs, crawl_limit):
    limit = crawl_limit
    doc_id = 0
    all_links = []
    url_html_dict = {}
    last_domain = None
    seed_done = False
    incr = 0
    URL_frontier = deque()
    
    for url in URLs:
        URL_frontier.append(url)
    
    while len(url_html_dict) < limit and URL_frontier:
        # Simple random choice - either take from left or right
        if seed_done:
            current_url = (URL_frontier.popleft() if random.random() < 0.5 
                          else URL_frontier.pop())
        else:
            current_url = (URL_frontier.popleft())
            incr = incr + 1
            if incr == len(URLs):
                print(f"DONE WITH SEEDINGS")
                seed_done = True
        
        current_domain = get_base_domain(current_url)
        
        if current_domain == last_domain:
            different_domain_url = find_different_domain_url(URL_frontier, current_domain)
            
            if different_domain_url:
                URL_frontier.append(current_url)
                current_url = different_domain_url
                current_domain = get_base_domain(current_url)
            else:
                print(f"No different domains available, sleeping for 2 seconds...")
                time.sleep(2)
        
        politeness_rules = Robotparser(current_url, "*")
        
        if not url_filter(current_url, politeness_rules):
            continue
        
        soup, html_content = fetch_html(current_url)
        print(f"Processing URL: {current_url} - Queue length: {len(URL_frontier)}")
        
        if soup:
            links = extract_links(soup, current_url)
            for link in links:
                if link not in URL_frontier:
                    # Randomly add to left or right of deque
                    URL_frontier.append(link)
                if link not in all_links:
                    all_links.append(link)
            store_in_dict(current_url, html_content, url_html_dict, links, doc_id)
            doc_id += 1
            print(f"NUMBER OF DOCUMENTS ADDED: {doc_id}\n\n")
        
        last_domain = current_domain
    
    print("Finished crawling.")
    url_html_dict["all_links"] = all_links
    with open("crawled_data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(url_html_dict, indent=4))
