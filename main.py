import argparse
import asyncio
import json
from Lektion02.crawler import start_crawler, URL_seed
from Lektion03.indexer import start_indexing
from Lektion03.querier import start_query, get_links
from Lektion04.ranker_v1 import start_ranker_v1
from Lektion05.ranker_v2 import start_ranker_v2

parser = argparse.ArgumentParser()

parser.add_argument('-q', '--query', help="Start query", action='store_true')
parser.add_argument('-c', '--crawl', help="Start crawler", action='store_true')
parser.add_argument('-i', '--index', help="Start indexer", action='store_true')

args = parser.parse_args()
limit = 10

if __name__ == "__main__":
    if args.crawl:
        # Run the crawling process
        asyncio.run(start_crawler(URL_seed))

    if args.index:
        with open("crawled_data.json", "r") as file:
            content = json.load(file)
        start_indexing(content)
        
    if args.query:
        QUERY = "nyheder og information"
        print(f"QUERYING: {QUERY}")
        scores = start_query(QUERY)
        # ranked_pages_v1 = start_ranker_v1(scores)
        # links = get_links(ranked_pages_v2, limit)
        ranked_pages_v2 = start_ranker_v2(scores)
        print(ranked_pages_v2[:limit])
        print("\n\n")
        QUERY = "insurance and vacation"
        print(f"QUERYING: {QUERY}")
        scores = start_query(QUERY)
        # ranked_pages_v1 = start_ranker_v1(scores)
        # links = get_links(ranked_pages_v2, limit)
        ranked_pages_v2 = start_ranker_v2(scores)
        print(ranked_pages_v2[:limit])
