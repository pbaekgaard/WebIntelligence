import argparse
import asyncio
import json

from Lektion02.crawler import URL_seed, start_crawler
from Lektion03.indexer import start_indexing
from Lektion03.querier import get_links, start_query
from Lektion04.ranker_v1 import VSM
from Lektion05.ranker_v2 import PageRank, rank_pages_with_pagerank
from rankers.aggregated import aggregate

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
        asyncio.run(start_crawler(URL_seed, crawl_limit=200))

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
        # query_results = start_query(QUERY)
        #
        # ranked_query_results = VSM(QUERY,query_results)
        # print(f"RESULT FROM QUERY: {QUERY}\n")
        # print(ranked_query_results)
        # print("\n\n")
        #
        # query_results = start_query(QUERY2)
        #
        # ranked_query_results = VSM(QUERY2,query_results)
        # print(f"RESULT FROM QUERY: {QUERY2}\n")
        # print(ranked_query_results)
        # print("\n\n")



        # Query and rank using PageRank
        # ranked_pages_v2 = PageRank(content)
        #
        # print(f"QUERYING USING PAGERANK: {QUERY}")
        # query_results = start_query(QUERY)
        # query_links = get_links(query_results, limit)
        # results = rank_pages_with_pagerank(query_links)
        # print(f"RESULTS: {results}")
        #
        # print(f"QUERYING USING PAGERANK: {QUERY2}")
        # query_results = start_query(QUERY2)
        # query_links = get_links(query_results, limit)
        # results = rank_pages_with_pagerank(query_links)
        # print(f"RESULTS: {results}")
        #
        # Query and rank using Aggregated VSM and PageRank
        page_ranked_content = PageRank(content)
        query_results = start_query(QUERY)
        vsm_results = VSM(QUERY,query_results)
        aggregated_results = aggregate(vsm_results, page_ranked_content)



