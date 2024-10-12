import math
from collections import defaultdict

class SearchEngine:
    def __init__(self, index):
        self.index = index
        self.all_docs = set(docid for term in self.index for docid in self.index[term])

    def BooleanQueryProcessor(self, query):
        query = query.lower().split()
        if not query:
            return set()

        result = self.evaluate_term(query[0])
        i = 1
        while i < len(query):
            if query[i] == 'and':
                i += 1
                if i < len(query):
                    result &= self.evaluate_term(query[i])
                else:
                    raise ValueError("'and' operator is missing a right operand")
            elif query[i] == 'or':
                i += 1
                if i < len(query):
                    result |= self.evaluate_term(query[i])
                else:
                    raise ValueError("'or' operator is missing a right operand")
            elif query[i] == 'not':
                i += 1
                if i < len(query):
                    result -= self.evaluate_term(query[i])
                else:
                    raise ValueError("'not' operator is missing an operand")
            else:
                result &= self.evaluate_term(query[i])
            i += 1

        return result

    def evaluate_term(self, term):
        if term == 'not':
            raise ValueError("'not' cannot be used as a standalone term")
        return set(self.index.get(term.lower(), {}).keys())

    def Search(self, query, num_res):
        # Tokenize the query
        tokens = query.lower().split()
        queryTerms = [token for token in tokens if token not in ['and', 'or', 'not']]

        # Get documents that satisfy the query using Boolean Query Processing
        doc_list = self.BooleanQueryProcessor(query)
        print("Documents satisfying boolean query:", doc_list)

        # Initialize a dictionary to store document scores
        doc_scores = defaultdict(float)

        # Number of documents in the index (for IDF calculation)
        NUM_DOCS = len(self.all_docs)

        # Query term frequency
        query_tf = defaultdict(int)
        for term in queryTerms:
            query_tf[term] += 1

        # Calculate the scores for each document
        for term in queryTerms:
            if term in self.index:
                doc_freq = len(self.index[term])

                for docid in doc_list:
                    if docid in self.index[term]:
                        # Calculate the term frequency in the query
                        tf_query = query_tf[term]
                        
                        # Calculate normwt for the query term
                        normwt_query = (1 + math.log10(tf_query)) * math.log10(NUM_DOCS / doc_freq)

                        # Get document's normalized weight (norm_wt) from the index
                        doc_normwt = self.index[term][docid]['norm_wt']
                        
                        # Add to document score: normwt_query * norm_wt (LNC-LTC)
                        doc_scores[docid] += normwt_query * doc_normwt

        # Sort documents by their scores in descending order
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

        print("Scored documents:", sorted_docs)

        # Return the top-K results (top num_res results)
        return sorted_docs[:num_res]

# Test the implementation
index = {
    'best': {0: {'wt': 1.0, 'norm_wt': 0.5}},
    'car': {0: {'wt': 1.0, 'norm_wt': 0.5203903311516482}},
    'insurance': {0: {'wt': 1.3010299956639813, 'norm_wt': 0.6770434302818067}},
    'auto': {0: {'wt': 1.0, 'norm_wt': 0.5203903311516482}}
}
