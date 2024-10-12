class BooleanQueryProcessor:
    def __init__(self, index):
        self.index = index
        self.all_docs = set(doc_id for term in self.index for doc_id in self.index[term])

    def process_query(self, query):
        query = query.lower().split()
        if not query:
            return []

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
                raise ValueError(f"Unknown operator or term: {query[i]}")
            i += 1

        return list(result)

    def evaluate_term(self, term):
        if term == 'not':
            raise ValueError("'not' cannot be used as a standalone term")
        return set(self.index.get(term, {}).keys())

# Example usage
index = {
    'car': {0: {'wt': 1.0, 'norm_wt': 0.5203903311516482}, 1: {'wt': 1.0, 'norm_wt': 0.5}},
    'insurance': {0: {'wt': 1.3010299956639813, 'norm_wt': 0.6770434302818067}, 2: {'wt': 1.0, 'norm_wt': 0.7}},
    'auto': {0: {'wt': 1.0, 'norm_wt': 0.5203903311516482}, 1: {'wt': 1.0, 'norm_wt': 0.5}, 3: {'wt': 1.0, 'norm_wt': 0.6}}
}

processor = BooleanQueryProcessor(index)

# Test queries
queries = [
    "car and insurance",
    "car or auto",
    "insurance and not auto",
    "car and not insurance",
    "auto or insurance and not car"
]

for query in queries:
    try:
        result = processor.process_query(query)
        print(f"Query: {query}")
        print(f"Result: {result}\n")
    except ValueError as e:
        print(f"Query: {query}")
        print(f"Error: {str(e)}\n")
