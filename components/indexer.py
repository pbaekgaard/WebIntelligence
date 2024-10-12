
import re
import math
from collections import defaultdict
from bs4 import BeautifulSoup

class Indexer:
    def __init__(self, stop_words=None):
        self.index = defaultdict(dict)  # Term -> list of (doc_id, lnc)
        self.documents = {}              # doc_id -> tokens
        self.doc_lengths = {}            # doc_id -> length for cosine normalization
        self.doc_freq = defaultdict(int)  # Term -> document frequency (df)
        self.total_docs = 0              # Total number of documents
        
        if stop_words is None:
            self.stop_words = set([
                "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
                "to", "was", "were", "will", "with"
            ])

    def tokenize(self, text):
        # Convert to lowercase and split on non-alphanumeric characters
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def get_tokens(self, text):
        # Remove HTML tags and tokenize
        text = BeautifulSoup(text, "html.parser").get_text()
        tokens = self.tokenize(text)
        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens

    def add_document(self, doc_id, content):
        tokens = self.get_tokens(content)
        self.documents[doc_id] = tokens
        self.total_docs += 1
        
        # Compute term frequencies (tf) for this document
        tf = defaultdict(int)
        for token in tokens:
            tf[token] += 1
        
        # Update document frequency (df) for each term
        unique_terms = set(tokens)
        for term in unique_terms:
            self.doc_freq[term] += 1

        # Store lnc (Logarithmic Normalized Count) in the index
        self.doc_lengths[doc_id] = 0  # Initialize document length for normalization
        for term, freq in tf.items():
            #INFO: Calculates the LN part of LNC
            tf_raw = freq
            tfSTAR_wt = 1+math.log10(tf_raw)
            wt = tfSTAR_wt * 1 if freq > 0 else 0
            self.index[term].setdefault(doc_id, {"wt": wt})
            
            # Update document length (sum of squared term weights)
            self.doc_lengths[doc_id] += wt ** 2

        # Normalize document length (for cosine normalization)
        # INFO: Calculates the Cosine Normalization of the LN part = LNC
        for term, freq in tf.items():
            self.index[term][doc_id]['norm_wt'] = self.index[term][doc_id]['wt']*(1/(math.sqrt(self.doc_lengths[doc_id])))

    def idf(self, term):
        # Calculate inverse document frequency (idf)
        if term in self.doc_freq:
            return math.log10(self.total_docs / self.doc_freq[term]) if self.doc_freq[term] > 0 else 0
        return 0

    def get_index(self):
        return dict(self.index)
