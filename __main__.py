from components.BooleanQueryProcessor import BooleanQueryProcessor
from components.crawler import Crawler
from components.indexer import Indexer
from components.search import SearchEngine
import json

# Global Variables
PAGES_SIZE = 100  # You can change this value to set the number of pages to crawl
SEED_URL = "https://dr.dk/"  # Change to your seed URL
SEED_URLS = [
    "https://www.dr.dk",
    "https://tv2.dk",
    "https://politiken.dk",
    "https://ekstrabladet.dk",
    "https://www.berlingske.dk",
    "https://www.information.dk",
    "https://videnskab.dk",
    "https://www.au.dk",
    "https://www.cbs.dk",
    "https://www.kum.dk",
    "https://www.dr.dk/p4",
    "https://www.visitdenmark.dk",
    "https://www.ku.dk",
    "https://www.dst.dk",
    "https://www.regeringen.dk",
    "https://www.sundhed.dk",
    "https://www.boligsiden.dk",
    "https://www.jobindex.dk",
    "https://www.dba.dk",
    "https://www.danskindustri.dk"
]
STOP_WORDS = {
}

def main():
    # Initialize the crawler
    crawler = Crawler(pages_size=PAGES_SIZE, seed_urls=SEED_URLS)
    # Run the crawler
    pages = crawler.crawl()
    # Create an inverted index:
    ## Initialize the Indexer
    indexer = Indexer()
    for url, content in pages.items():
        indexer.add_document(url, content)

    with open("index.json", "w") as outfile:
        json.dump(indexer.get_index(), outfile)

    searchEngine = SearchEngine(indexer.get_index())
    query = "norlys AND danmark"
    result = searchEngine.Search(query, num_res=3)
    print(result)

if __name__ == "__main__":
    main()

