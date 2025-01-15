# Dictionary to store URLs and their HTML content
# In your crawler.py
from Lektion01.Exercise1 import jaccard_similarity_normal


def store_in_dict(url, html_content, url_html_dict, links, doc_id):
    """Stores the HTML content and URL in the dictionary if the similarity check passes."""
    # Parameters for the similarity check
    N = 5  # Example parameter value for the shingle size
    for stored_url, stored_html in url_html_dict.items():
        similarity = jaccard_similarity_normal(html_content, stored_html[1], N)
        if similarity >= 0.85:
            print(f"HTML content for {url} is similar to {stored_url} (Similarity: {similarity}). Not storing.")
            return # Skip storing if similarity is above the threshold

    # Store if no similar content is found
    links_as_list = list(links)
    url_html_dict[url] = [doc_id, html_content, links_as_list]
    print(f"Stored document for URL: {url}")
    



