import numpy as np


def aggregate(vsm_results, page_rank_content, beta=0.5):
    # Create a dictionary for quick lookup of PageRank scores by URL
    page_rank_dict = dict(page_rank_content)

    # Prepare the aggregated scores
    aggregated_scores = {}

    # Iterate over the VSM results to combine with the PageRank scores
    for url, vsm_score in vsm_results:
        # Get the corresponding PageRank score (default to 0 if not found)
        page_rank_score = page_rank_dict.get(url, 0)

        # Apply the formula to combine VSM and PageRank scores
        aggregated_score = (beta * vsm_score) + ((1 - beta) * page_rank_score)

        # Store the aggregated score
        aggregated_scores[url] = aggregated_score

    return aggregated_scores
