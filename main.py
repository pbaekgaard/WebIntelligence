import argparse
import asyncio
import json

from components.crawler.crawler import URL_seed, start_crawler
from components.indexer import start_indexing
from components.querier import get_links, start_query
from components.rankers.aggregated import aggregate
from components.rankers.pagerank import PageRank, rank_pages_with_pagerank
from components.rankers.vsm import VSM

parser = argparse.ArgumentParser()

parser.add_argument('-q', '--query', help="Start query", action='store_true')
parser.add_argument('-c', '--crawl', help="Start crawler", action='store_true')
parser.add_argument('-i', '--index', help="Start indexer", action='store_true')

args = parser.parse_args()
limit = 10
URL_seed = [
    "https://www.allianztravelinsurance.com",
    "https://cphpost.dk/",
    "https://www.travelguard.com/",
    "https://www.bbc.com/news",
]
if __name__ == "__main__":
    if args.crawl:
        # Run the crawling process
        # print(URL_seed)
        asyncio.run(start_crawler(URL_seed, crawl_limit=2))

    if args.index:
        with open("crawled_data.json", "r") as file:
            content = json.load(file)
        start_indexing(content)
        
    if args.query:
        with open("crawled_data.json", "r") as file:
            content = json.load(file)
        QUERY = "world news and information and politics"
        QUERY2 = "insurance and vacation"

        # Query and rank using VSM

        print("=" * 50)
        print(" " * 19 + "VSM RESULTS" + " " * 19)
        print("=" * 50)
        query_results = start_query(QUERY)

        ranked_query_results = VSM(QUERY,query_results)
        print(f"RESULT FROM QUERY: {QUERY}\n")
        print(ranked_query_results)
        print("\n")

        query_results = start_query(QUERY2)

        ranked_query_results = VSM(QUERY2,query_results)
        print(f"RESULT FROM QUERY: {QUERY2}\n")
        print(ranked_query_results)
        print("\n\n\n\n")



        # Query and rank using PageRank
        print("=" * 50)
        print(" " * 17 + "PAGERANK RESULTS" + " " * 16)
        print("=" * 50)
        ranked_pages_v2 = PageRank(content)

        print(f"QUERYING USING PAGERANK: {QUERY}")
        query_results = start_query(QUERY)
        query_links = get_links(query_results, limit)
        results = rank_pages_with_pagerank(query_links)
        print(f"RESULTS: {results}\n")

        print(f"QUERYING USING PAGERANK: {QUERY2}")
        query_results = start_query(QUERY2)
        query_links = get_links(query_results, limit)
        results = rank_pages_with_pagerank(query_links)
        print(f"RESULTS: {results}")
        print("\n\n\n\n")

        # Query and rank using Aggregated VSM and PageRank
        print("=" * 50)
        print(" " * 17 + "AGGREGATED RESULTS" + " " * 16)
        print("=" * 50)
        page_ranked_content = PageRank(content)
        print(f"QUERYING USING AGGREGATED: {QUERY}")
        query_results = start_query(QUERY)
        vsm_results = VSM(QUERY,query_results)
        aggregated_results = aggregate(vsm_results, page_ranked_content)
        print(aggregated_results[:limit])
        print("\n")


        print(f"QUERYING USING AGGREGATED: {QUERY2}")
        query_results = start_query(QUERY2)
        vsm_results = VSM(QUERY,query_results)
        aggregated_results = aggregate(vsm_results, page_ranked_content)
        print(aggregated_results[:limit])



