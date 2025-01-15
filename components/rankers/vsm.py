import json
import math
import re

from nltk.stem import PorterStemmer


def stemming(word):
    ps = PorterStemmer()
    return ps.stem(word)

def VSM(query, query_results):
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)

    scores = {}
    query_freq = {}
    idf = {}
    doc_length = 0

    complete_stemmed_query = []
    for word in query.split():
        complete_stemmed_query.append(stemming(word))

    for word in complete_stemmed_query:
        idf[word] = inverted_index[word]["idf"] if word in inverted_index else 0
        weight = idf[word]
        if word not in query_freq:
            occurences = len(re.findall(word, " ".join(complete_stemmed_query)))
            query_freq[word] = 0 if occurences == 0 else (1 + math.log10(occurences)) * weight

    for word, wt in query_freq.items():
        doc_length += pow(wt, 2)

    doc_length = math.sqrt(doc_length)

    for word, wt_query in query_freq.items():
        query_freq[word] = wt_query / doc_length # Norm wt
        for doc in inverted_index[word]["doc_ids"]:
            for doc_id, wt_index in doc.items():
                if doc_id not in scores:
                    scores[doc_id] = 0
                scores[doc_id] += wt_index * wt_query


    scores = filter_scores_by_query_results(query_results, scores)
    scores = to_links(scores)
    scores = start_ranker_v1(scores)
    return scores


def to_links(scores):
    # Load the crawled data
    with open("crawled_data.json", "r") as file:
        crawled_data = json.load(file)

    # Create a dictionary for fast lookup by id
    id_to_url = {content[0]: url for url, content in crawled_data.items()}

    # Replace the ids in scores with their corresponding URLs and keep the same format
    result_with_links = {
        id_to_url.get(int(doc_id), f"ID-{doc_id}-NOT-FOUND"): score
        for doc_id, score in scores.items()
    }

    return result_with_links


def filter_scores_by_query_results(query_results, scores):
    # Convert query_results to string to match the keys in scores
    query_results_str = set(map(str, query_results))

    # Filter scores by keys present in query_results
    filtered_scores = {doc_id: score for doc_id, score in scores.items() if doc_id in query_results_str}

    return filtered_scores

def start_ranker_v1(scores):
    return sorted(scores.items(), key=lambda x:x[1], reverse=True)
