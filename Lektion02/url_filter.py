from urllib.parse import urlparse

def url_filter(url, politeness_rules):
    """Check if the given URL can be crawled based on politeness rules."""
    if not politeness_rules:
        return True  # No politeness rules, so assume crawling is allowed
    
    disallowed_paths = politeness_rules.get("Disallow", [])
    crawl_delay = politeness_rules.get("Crawl-delay", None)

    if disallowed_paths:
        parsed_url = urlparse(url)
        path = parsed_url.path
        if any(path.startswith(d) for d in disallowed_paths):
            print(f"Crawling disallowed for {url}")
            return False
    
    return True
