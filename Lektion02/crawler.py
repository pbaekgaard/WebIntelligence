import asyncio
import json
from urllib.parse import urlparse
from .RobotParser import Robotparser
from .DuplicateURL import duplicateUrl
from .url_filter import url_filter
from .DocFPs import store_in_dict
from .fetch_pageandlink import extract_links, fetch_html

URL_seed = [
    "https://www.insuremytrip.com/",
    "https://www.dr.dk/",
]

URL_frontier = []

async def start_crawler(URLs):
    limit = 8
    doc_id = 0
    all_links = []
    url_html_dict = {}
    URL_frontier.extend(URLs)

    while len(url_html_dict) < limit and URL_frontier:
        url = URL_frontier.pop(0)
        politeness_rules = Robotparser(url, "*")
        
        # Use the function to check if crawling is allowed
        if not url_filter(url, politeness_rules):
            continue
        
        # Fetch and parse HTML page
        soup, html_content = fetch_html(url)
        print(f"Processing URL: {url} - Queue length: {len(URL_frontier)}")
        if soup:
            links = extract_links(soup, url)
            for link in links:
                if link not in URL_frontier:  # Avoid adding duplicates
                    URL_frontier.append(link)
                if link not in all_links:
                    all_links.append(link)
            store_in_dict(url, html_content, url_html_dict, links, doc_id)
            doc_id += 1
    
    print("Finished crawling.")
    url_html_dict["all_links"] = all_links

    with open("crawled_data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(url_html_dict, indent=4))
