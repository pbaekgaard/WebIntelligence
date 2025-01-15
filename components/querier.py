import json
import math
import re

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def clean_input_strings(input: str):
    # Remove punctuation
    replace_pattern = "[.,!?;():\[\]{}'\"]"
    input_string = re.sub(replace_pattern, "", input)
    return input_string

def query_intersect(word1, word2):
    answer = []
    index_word1 = 0
    index_word2 = 0
    while index_word1 < len(word1["doc_ids"]) and index_word2 < len(word2["doc_ids"]):
        if word1["doc_ids"][index_word1] == word2["doc_ids"][index_word2]:
            answer.append(word1["doc_ids"][index_word1])
            index_word1 += 1
            index_word2 += 1
        elif word1["doc_ids"][index_word1] < word2["doc_ids"][index_word2]:
            index_word1 += 1
        elif word1["doc_ids"][index_word1] > word2["doc_ids"][index_word2]:
            index_word2 += 1

    return answer

def query_or(word1, word2):
    answer = []
    index_word1 = 0
    index_word2 = 0
    while index_word1 < len(word1["doc_ids"]) and index_word2 < len(word2["doc_ids"]):
        if word1["doc_ids"][index_word1] == word2["doc_ids"][index_word2]:
            answer.append(word1["doc_ids"][index_word1])
            index_word1 += 1
            index_word2 += 1
        elif word1["doc_ids"][index_word1] < word2["doc_ids"][index_word2]:
            answer.append(word1["doc_ids"][index_word1])
            index_word1 += 1
        elif word1["doc_ids"][index_word1] > word2["doc_ids"][index_word2]:
            answer.append(word2["doc_ids"][index_word2])
            index_word2 += 1
    while index_word1 < len(word1["doc_ids"]):
        answer.append(word1["doc_ids"][index_word1])
        index_word1 += 1

    while index_word2 < len(word2["doc_ids"]):
        answer.append(word2["doc_ids"][index_word2])
        index_word2 += 1

    return answer

def query_and_not(word1, word2):
    answer = []
    index_word1 = 0
    index_word2 = 0
    while index_word1 < len(word1["doc_ids"]) and index_word2 < len(word2["doc_ids"]):
        if word1["doc_ids"][index_word1] == word2["doc_ids"][index_word2]:
            index_word1 += 1
            index_word2 += 1
        elif word1["doc_ids"][index_word1] < word2["doc_ids"][index_word2]:
            answer.append(word1["doc_ids"][index_word1])
            index_word1 += 1
        elif word1["doc_ids"][index_word1] > word2["doc_ids"][index_word2]:
            index_word2 += 1

    while index_word1 < len(word1["doc_ids"]):
        answer.append(word1["doc_ids"][index_word1])
        index_word1 += 1

    return answer

def querier_v1(query):
    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)
    complete_stemmed_query = stem_query(query, True)

    complete_stemmed_query = replace_words(inverted_index, complete_stemmed_query)

    complete_query = []
    # Order so that or are first and then order the and based on document frequencies
    for index, token in enumerate(complete_stemmed_query):
        if token == "or":
            # If first term is an OR
            if index <= 2:
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, True))

            # For all other terms than the first term
            if index > 2 and (complete_stemmed_query[index - 2] == "or" or complete_stemmed_query[index - 3] == "or"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))
            elif index > 2 and (complete_stemmed_query[index - 2] != "or" or complete_stemmed_query[index - 3] != "or"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, True))

    # Insert implicit ANDs
    for index, token in enumerate(complete_stemmed_query):
        if token == "and":
            # If first term is an AND
            if index <= 2:
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, True))

            # Only add the token if at least one of the surrounding terms are an OR
            elif index > 2 and index + 3 < len(complete_stemmed_query) and (complete_stemmed_query[index + 2] == "or" or complete_stemmed_query[index + 3] == "or" \
               or complete_stemmed_query[index - 2] == "or" or complete_stemmed_query[index - 3] == "or"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))

            elif index > 2 and (complete_stemmed_query[index - 2] == "or" or complete_stemmed_query[index - 3] == "or"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))
            
            elif index + 3 < len(complete_stemmed_query) and (complete_stemmed_query[index + 2] == "or" or complete_stemmed_query[index + 3] == "or"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))


            # For all terms except the first and the last term
            elif index > 2 and index + 3 < len(complete_stemmed_query) and (complete_stemmed_query[index + 2] == "and" or complete_stemmed_query[index + 3] == "and") \
               and (complete_stemmed_query[index - 2] == "and" or complete_stemmed_query[index - 3] == "and"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))
            elif index > 2 and index + 3 < len(complete_stemmed_query) and (complete_stemmed_query[index + 2] == "and" or complete_stemmed_query[index + 3] == "and") \
                 and (complete_stemmed_query[index - 2] != "and" or complete_stemmed_query[index - 3] != "and"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, True))
            
            # If the last term is an AND
            elif index > 2 and (complete_stemmed_query[index - 2] == "and" or complete_stemmed_query[index - 3] == "and"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, False))
            elif index > 2 and (complete_stemmed_query[index - 2] != "and" or complete_stemmed_query[index - 3] != "and"):
                complete_query.extend(add_words_to_complete_query(complete_stemmed_query, index, True))

    # Find all occurrences of OR terms in the complete query
    occurences_or = [i for i, token in enumerate(complete_query) if token == "or"]

    # Insert AND between OR terms that have no term (e.g. top or home rise or sale -> top or home and rise or sale)
    for occurence_or in occurences_or:
        if occurence_or + 3 < len(complete_query) and (complete_query[occurence_or + 2] != "and" and complete_query[occurence_or + 3] != "and"):
            if complete_query[occurence_or + 1] == "not":
                complete_query.insert(occurence_or + 3, "and")
            else:    
                complete_query.insert(occurence_or + 2, "and")

    # Find the new indexes for all OR terms in the complete query
    occurences_or = [i for i, token in enumerate(complete_query) if token == "or"]

    # Query all OR terms
    with open("crawled_data.json", "r") as file:
        complete_list_of_doc_ids = [content[0] for link, content in json.load(file).items()]

    temp_query = []
    for occurence_or in reversed(occurences_or):
        new_term = {}
        
        if occurence_or + 2 < len(complete_query) and complete_query[occurence_or + 1] == "not" and \
           occurence_or - 2 >= 0 and complete_query[occurence_or - 2] == "not":
            # Find all documents that it does not appear in
            complement_or_1 = [i for i in complete_list_of_doc_ids if i not in complete_query[occurence_or + 2]["doc_ids"]]
            complement_or_2 = [i for i in complete_list_of_doc_ids if i not in complete_query[occurence_or - 1]["doc_ids"]]
            complete_query[occurence_or + 2] = {
                "doc_freq": len(complement_or_1),
                "doc_ids": complement_or_1
                }
            complete_query[occurence_or - 1] = {
                "doc_freq": len(complement_or_2),
                "doc_ids": complement_or_2
                }
            result = query_or(complete_query[occurence_or - 1], complete_query[occurence_or + 2])
            new_term["pop_times"] = 5
            new_term["pop"] = occurence_or - 1

        elif occurence_or + 2 < len(complete_query) and complete_query[occurence_or + 1] == "not":
            # Find all documents that it does not appear in
            complement_or = [i for i in complete_list_of_doc_ids if i not in complete_query[occurence_or + 2]["doc_ids"]]
            complete_query[occurence_or + 2] = {
                "doc_freq": len(complement_or),
                "doc_ids": complement_or
                }
            result = query_or(complete_query[occurence_or - 1], complete_query[occurence_or + 2])
            new_term["pop_times"] = 4
            new_term["pop"] = occurence_or

        elif occurence_or - 2 >= 0 and complete_query[occurence_or - 2] == "not":
            # Find all documents that it does not appear in
            complement_or = [i for i in complete_list_of_doc_ids if i not in complete_query[occurence_or - 1]["doc_ids"]]
            complete_query[occurence_or - 1] = {
                "doc_freq": len(complement_or),
                "doc_ids": complement_or
                }
            result = query_or(complete_query[occurence_or - 1], complete_query[occurence_or + 1])
            new_term["pop_times"] = 4
            new_term["pop"] = occurence_or - 1

        else:
            result = query_or(complete_query[occurence_or - 1], complete_query[occurence_or + 1])
            new_term["pop_times"] = 3
            new_term["pop"] = occurence_or

        new_term["doc_freq"] = len(result)
        new_term["doc_ids"] = result
        temp_query.append(new_term)

    # Replace OR terms with their results in the complete query
    for index, occurence_or in enumerate(reversed(occurences_or)):
        complete_query.insert(temp_query[index]["pop"] - 1, temp_query[index])
        for i in range(temp_query[index]["pop_times"]):
            complete_query.pop(temp_query[index]["pop"])

    occurences_not = [i for i, token in enumerate(complete_query) if token == "not" and complete_query[i - 1] == "and"]
    
    # Query all AND NOT terms
    temp_query = []
    for occurence_not in reversed(occurences_not):
        new_term = {}
        if occurence_not - 2 >= 0 and occurence_not + 1 < len(complete_query):
            result = query_and_not(complete_query[occurence_not - 2], complete_query[occurence_not + 1])
            new_term["pop_times"] = 4
            new_term["doc_freq"] = len(result)
            new_term["doc_ids"] = result
            temp_query.append(new_term)

    # Replace AND NOT terms with their results in the complete query
    for index, occurence_not in enumerate(reversed(occurences_not)):
        complete_query.insert(occurence_not - 2, temp_query[index])
        for i in range(temp_query[index]["pop_times"]):
            complete_query.pop(occurence_not - 1)

    # Order the complete list
    complete_query: list = order_query_list(complete_query)

    # Query all AND terms
    while len(complete_query) > 1:
        # Find first occurence of AND in the complete query
        and_index = complete_query.index("and")
        new_term = {}
        if and_index + 2 < len(complete_query) and complete_query[and_index + 1] == "not":
            result = query_and_not(complete_query[and_index - 1], complete_query[and_index + 2])
            new_term["pop_times"] = 4
        else:
            result = query_intersect(complete_query[and_index - 1], complete_query[and_index + 1])
            new_term["pop_times"] = 3
        new_term["doc_freq"] = len(result)
        new_term["doc_ids"] = result
        
        # Replace the AND term with its results in the complete query and reorder the list of terms based on document frequency
        complete_query.insert(and_index - 1, new_term)
        for i in range(new_term["pop_times"]):
            complete_query.pop(and_index)
        complete_query: list = order_query_list(complete_query)

    return complete_query


def querier_v2(query):
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

    return scores

def querier_v4(query):
    def parse_query(query):
        """Parse the query to split it into tokens and identify operators."""
        tokens = query.split()
        parsed = []
        for token in tokens:
            if token.upper() in {"AND", "OR", "NOT"}:
                parsed.append(token.upper())
            else:
                parsed.append(stemming(token))  # Stem non-operator words
        return parsed

    def extract_doc_ids(doc_list):
        """Extract document IDs from the list of dictionaries."""
        return {int(list(doc.keys())[0]) for doc in doc_list}

    def process_query(parsed_query, inverted_index):
        """Evaluate the parsed query to find matching documents."""
        stack = []
        for token in parsed_query:
            if token == "AND":
                # Perform intersection between the last two sets
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a & b)
            elif token == "OR":
                # Perform union between the last two sets
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a | b)
            elif token == "NOT":
                # Perform subtraction of the last set from the one before it
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a - b)
            else:
                # Push the document set for the term onto the stack
                doc_ids = extract_doc_ids(inverted_index.get(token, {}).get("doc_ids", []))
                stack.append(doc_ids)
        
        # The final result should be the only set remaining in the stack
        return stack.pop() if stack else set()

    with open("inverted_index.json", "r") as file:
        inverted_index = json.load(file)

    parsed_query = parse_query(query)
    matching_docs = process_query(parsed_query, inverted_index)

    return list(matching_docs)

def stemming(word):
    ps = PorterStemmer()
    return ps.stem(word)

def stem_query(query, with_and):
    cleaned_input = clean_input_strings(query)
    tokenized_query = re.split("\s+", cleaned_input)
    stemmed_query = []
    complete_stemmed_query = []
    for token in tokenized_query:
        stemmed_query.append(ps.stem(token))

    for index, token in enumerate(stemmed_query):
        if with_and and (index - 1) >= 0 and token != "and" and token != "or" and token != "not" and stemmed_query[index - 1] != "and" and \
           stemmed_query[index - 1] != "or" and stemmed_query[index - 1] != "not":
            complete_stemmed_query.append("and")
            complete_stemmed_query.append(token)
        else:
            complete_stemmed_query.append(token)

    return complete_stemmed_query

def replace_words(inverted_index, complete_stemmed_query):
    # Find all document frequencies and posting listings (list of documents a word/token is in) 
    # and replace the corresponding token in the complete_stemmed_query array.
    for index, token in enumerate(complete_stemmed_query):
        if token != "and" and token != "or" and token != "not":
            if token not in inverted_index:
                complete_stemmed_query[index] = {
                    "doc_freq": 0,
                    "doc_ids": [],
                    "idf": 0,
                }
            else:
                complete_stemmed_query[index] = inverted_index[token] 
    return complete_stemmed_query

def order_query_list(complete_query):
    # Figure out what the ordering of the query tokens are based on the document frequency
    ordering_list = []
    for token in complete_query:
        if token != "and" and token != "or" and token != "not":
            ordering_list.append(token)
    ordering_list = sorted(ordering_list, key=lambda item: item["doc_freq"])

    # Order the complete list
    ordered_index = 0
    for index, token in enumerate(complete_query):
        if token != "and" and token != "or" and token != "not":
            complete_query[index] = ordering_list[ordered_index]
            ordered_index += 1
    return complete_query

def add_words_to_complete_query(query, index, full: bool):
    temp_query = []
    if index - 2 == 0 and query[index - 2] == "not":
        temp_query.append(query[index - 2])
    if full:
        temp_query.append(query[index - 1])
        temp_query.append(query[index])
        if query[index + 1] == "not":
            temp_query.append(query[index + 1])
            temp_query.append(query[index + 2])
        else:
            temp_query.append(query[index + 1])
    else:
        temp_query.append(query[index])
        if query[index + 1] == "not":
            temp_query.append(query[index + 1])
            temp_query.append(query[index + 2])
        else:
            temp_query.append(query[index + 1])
    return temp_query

def normalize_query(query):
    pass

def remove_stop_words(query):
    return " ".join([word for word in query.split() if word not in stopwords.words('english')])

def get_query():
    return "nyheder og information"

def get_links(doc_ids, limit):

    with open("crawled_data.json", "r") as file:
        file_content = json.load(file)
    links = []
    for id in doc_ids[:limit]:
        links.extend([link for link, content in file_content.items() if content[0] == int(id)])
    return links

def start_query(query):
    query = remove_stop_words(query)
    result = querier_v4(query)
    return result
