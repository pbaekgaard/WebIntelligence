from components.BooleanQueryProcessor import BooleanQueryProcessor
from components.crawler import Crawler
from components.indexer import Indexer

# Global Variables
PAGES_SIZE = 10  # You can change this value to set the number of pages to crawl
SEED_URL = "https://dr.dk/"  # Change to your seed URL
STOP_WORDS = {
}

def main():
    # Initialize the crawler
    crawler = Crawler(pages_size=PAGES_SIZE, seed_url=SEED_URL)
    # Run the crawler
    pages = crawler.crawl()
    # Create an inverted index:
    ## Initialize the Indexer
    indexer = Indexer()
    for url, content in pages.items():
        indexer.add_document(url, content)

    word_to_lookup = "ansvar"
    if word_to_lookup in indexer.index:
        print(f"Term: {word_to_lookup}")
        print(f"Postings: {indexer.index[word_to_lookup]}")
    else:
        print(f"'{word_to_lookup}' is not found in the index.")

if __name__ == "__main__":
    main()

