import re
import random

# Define a large prime number to be used in the permutation
LARGE_PRIME = 2**61 - 1

# Permute hash function using a random a, b (affine transformation)
def permute_hash(hash_value, a, b, prime=LARGE_PRIME):
    return (a * hash_value + b) % prime

# Generate k hash functions using the built-in hash and permutation
def generate_permuted_hash_functions(k):
    hash_functions = []
    for _ in range(k):
        a = random.randint(1, LARGE_PRIME - 1)  # Random coefficient a
        b = random.randint(0, LARGE_PRIME - 1)  # Random offset b

        # Create a new hash function by applying a permutation to the original hash
        hash_functions.append(lambda shingle, a=a, b=b: permute_hash(hash(shingle), a, b))
    return hash_functions

hash_functions = generate_permuted_hash_functions(84)

def clean_input_strings(input: str):
    # Remove punctuation
    replace_pattern = "[.,!?;():\[\]{}'\"]"
    input_string = re.sub(replace_pattern, "", input)
    return input_string

def jaccard_similarity_normal(doc1: str, doc2: str, shingles_size: int):
    doc1 = clean_input_strings(doc1)
    doc2 = clean_input_strings(doc2)

    # Create shingles
    shingles_doc_1 = create_shingle(doc1, shingles_size)
    shingles_doc_2 = create_shingle(doc2, shingles_size)

    # Compute Intersection
    intersec = shingles_doc_1.intersection(shingles_doc_2)

    # Compute Union
    union = shingles_doc_1.union(shingles_doc_2)

    jaccard_similarity = len(intersec) / len(union)

    return jaccard_similarity

# Trick 1:
def jaccard_similarity_1(doc1:str, doc2:str, shingles_size: int):

    # Remove punctuation
    doc1 = clean_input_strings(doc1)
    doc2 = clean_input_strings(doc2)

    # Create shingles
    shingles_doc_1 = create_shingle(doc1, shingles_size)
    shingles_doc_2 = create_shingle(doc2, shingles_size)

    # Find min hash
    min_hash_1 = [min([hash_fn(shingle) for shingle in shingles_doc_1]) for hash_fn in hash_functions]
    min_hash_2 = [min([hash_fn(shingle) for shingle in shingles_doc_2]) for hash_fn in hash_functions]

    # Compute Intersection
    intersec = 0
    for index, min_hash in enumerate(min_hash_1):
        if min_hash == min_hash_2[index]:
            intersec += 1

    # Compute Union
    union = len(min_hash_1)

    jaccard_similarity = intersec / union

    return jaccard_similarity

# Trick 2:
def jaccard_similarity_2(doc1:str, doc2:str, shingles_size: int, group_size: int):
    # Remove punctuation
    doc1 = clean_input_strings(doc1)
    doc2 = clean_input_strings(doc2)

    # Create shingles
    shingles_doc_1 = create_shingle(doc1, shingles_size)
    shingles_doc_2 = create_shingle(doc2, shingles_size)

    # Find min hash
    min_hash_1 = [min([hash_fn(shingle) for shingle in shingles_doc_1]) for hash_fn in hash_functions]
    min_hash_2 = [min([hash_fn(shingle) for shingle in shingles_doc_2]) for hash_fn in hash_functions]

    # Group into super-shingles
    super_shingles_1 = set([tuple(min_hash_1[i:i + group_size]) for i in range(0, len(min_hash_1), group_size)])
    super_shingles_2 = set([tuple(min_hash_2[i:i + group_size]) for i in range(0, len(min_hash_2), group_size)])

    #Hash each super-shingle
    hashed_super_shingle_1 = set([hash(super_shingle) for super_shingle in super_shingles_1])
    hashed_super_shingle_2 = set([hash(super_shingle) for super_shingle in super_shingles_2])

    # Compute Intersection
    intersec = hashed_super_shingle_1.intersection(hashed_super_shingle_2)

    jaccard_similarity = len(intersec)

    return jaccard_similarity

def create_shingle(doc, shingle_size):
    doc = re.split("\s+", doc)
    shingle_set = set()
    for index, word in enumerate(doc):
        if index + shingle_size > len(doc):
            break
        shingle_tuple = ()
        i = index
        while i < (index + shingle_size):
            shingle_tuple += (doc[i],)
            i += 1
        shingle_set.add(shingle_tuple)
    return shingle_set

doc_1 = "do not worry about your difficulties in mathematics"
doc_2 = "i would not worry about your difficulties, you can easily learn what is needed."
