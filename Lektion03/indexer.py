import re
import math
from nltk.stem import PorterStemmer
import json
import numpy as np

def clean_input_strings(input: str):
    # Remove punctuation
    replace_pattern = "[+*.,!?;():\[\]{}'\"]"
    input_string = re.sub(replace_pattern, "", input)
    return input_string

def tokenizer(input: str):
    cleaned_input = clean_input_strings(input)
    return re.split("\s+", cleaned_input)
    
def stemming(word):
    ps = PorterStemmer()
    return ps.stem(word)

def create_inverted_index(docs):
    inverted_index = {}
    inverted_index = {}
    temp_doc_info = []
    weight = 1
    for doc in docs:
        temp_doc = {}
        for word in doc["content"]:
            if word not in temp_doc:
                term_freq = len(re.findall(word, " ".join(doc["content"])))
                temp_doc[word] = 0 if term_freq == 0 else (1 + math.log10(term_freq)) * weight

            if word not in inverted_index:
                inverted_index[word] = {
                    "doc_freq": 0,
                    "doc_ids": []
                }
            list_of_doc_ids = [doc_id for doc in inverted_index[word]["doc_ids"] for doc_id in doc]
            if doc["doc_id"] not in list_of_doc_ids: 
                inverted_index[word]["doc_freq"] += 1
                doc_id = {
                    doc["doc_id"]: temp_doc[word],
                }
                inverted_index[word]["doc_ids"].append(doc_id)
        temp_doc_info.append(temp_doc)

    
    for doc in temp_doc_info:
        doc_length = 0
        for word, wt in doc.items():
            doc_length += pow(wt, 2)
        doc_length = math.sqrt(doc_length)
        for word, wt in doc.items():
            doc[word] = wt / doc_length # Norm wt
            for docu in inverted_index[word]["doc_ids"]:
                for key, value in docu.items():
                    docu[key] = doc[word]        

    for key, value in inverted_index.items():
        value["idf"] = math.log10(len(docs)/value["doc_freq"])

    return inverted_index

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

def start_indexing(doc_list):
    tokenized_docs = []
    stemmed_docs = []

    for link, content in doc_list.items():
        tokenized_doc = {}
        if link == "all_links":
            continue
        tokenized_doc["doc_id"] = content[0]
        tokenized_doc["content"] = tokenizer(content[1])
        tokenized_docs.append(tokenized_doc)

    for tokenized_doc in tokenized_docs:
        stemmed_doc = []
        stemmed_doc_with_id = {}
        for word in tokenized_doc["content"]:
            stemmed_doc.append(stemming(word))
        stemmed_doc_with_id["doc_id"] = tokenized_doc["doc_id"]
        stemmed_doc_with_id["content"] = stemmed_doc

        stemmed_docs.append(stemmed_doc_with_id)
        
    inverted_index = create_inverted_index(stemmed_docs)

    transition_matrix = get_transition_matrix(doc_list)

    transition_matrix = teleport_transition_matrix(transition_matrix)

    page_rankings = get_page_rankings(transition_matrix)

    page_rankings = add_links_to_rankings(doc_list, page_rankings)
    
    inverted_index["page_rankings"] = page_rankings

    with open("inverted_index.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(inverted_index, indent=4))
