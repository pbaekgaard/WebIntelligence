import json

import numpy as np


def get_transition_matrix(doc_list):
    all_links = doc_list["all_links"]
    page_rank_matrix = np.zeros((len(all_links), len(all_links)))
    for index, link in enumerate(all_links):
        if link in doc_list:
            for ref_link in doc_list[link][2]:
                page_rank_matrix[index][all_links.index(ref_link)] = 1/len(doc_list[link][2])
        else:
            for ref_index, ref_link in enumerate(all_links):
                if ref_link not in doc_list:
                    page_rank_matrix[index][ref_index] = 0

    
    return page_rank_matrix

def teleport_transition_matrix(transition_matrix):
    alpha = 0.1
    teleport_matrix = np.full(transition_matrix.shape, 1/transition_matrix.shape[0])
    zero_rows = np.all(transition_matrix == 0, axis=1)
    non_zero_rows = ~np.all(transition_matrix == 0, axis=1)
    transition_matrix[zero_rows] += teleport_matrix[zero_rows]
    transition_matrix[non_zero_rows] = (1-alpha)*transition_matrix[non_zero_rows] + alpha*teleport_matrix[non_zero_rows]
    return transition_matrix    
    

def get_page_rankings(transition_matrix):
    init_prob_dist = np.full((transition_matrix.shape[1],), 1/transition_matrix.shape[1])
    new_prob_dist = np.full((transition_matrix.shape[1],), 0)
    while not np.array_equal(init_prob_dist, new_prob_dist):
        new_prob_dist = np.dot(init_prob_dist, transition_matrix)
        init_prob_dist = np.copy(new_prob_dist)
    return new_prob_dist

def add_links_to_rankings(doc_list, page_rankings):
    new_page_rankings = [None]*len(page_rankings)
    for index, page_rank in enumerate(page_rankings):
        new_page_rankings[index] = (doc_list["all_links"][index], page_rank)
    return new_page_rankings

def PageRank(doc_list):
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)

    with open("crawled_data.json", "r") as file:
        crawled_data = json.load(file)
    
    transition_matrix = get_transition_matrix(doc_list)

    transition_matrix = teleport_transition_matrix(transition_matrix)

    page_rankings = get_page_rankings(transition_matrix)

    page_rankings = add_links_to_rankings(doc_list, page_rankings)

    inverted_index["page_rankings"] = page_rankings

    with open("inverted_index.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(inverted_index, indent=4))
    # print(inverted_index["page_rankings"])
    return inverted_index


def get_ranked_scores(scores):
    return sorted(scores.items(), key=lambda x:x[1], reverse=True)
    


def rank_pages_with_pagerank(matching_docs):
    # Load the inverted index
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)

    # Get the PageRank scores
    pagerank_scores = inverted_index['page_rankings']

    # Sort the pages by their PageRank scores in descending order (reverse=True for descending)
    ranked_pages = sorted(
        pagerank_scores,
        key=lambda item: item[1],  # Sort by the PageRank score (index 1 of each tuple)
        reverse=True  # Sort from highest to lowest score
    )

    # Filter only pages that match the query results (matching_docs is a set of document IDs)
    filtered_ranked_pages = [(page, score) for page, score in ranked_pages if page in matching_docs]

    return filtered_ranked_pages
