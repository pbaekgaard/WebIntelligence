import re
import hashlib

class Jaccard:
    def __init__(self):
        self.shingle_size = 3
        self.sketch_size = 84

    def near_duplicate(self, content, index, SIMILARITY_THRESHOLD):
        for _, indexed_html in index.items():
            jaccardResult = self.is_near_duplicate(content, indexed_html)
            if jaccardResult >= SIMILARITY_THRESHOLD:
                return True
        return False

    def is_near_duplicate(self, content, indexed_html):
        contentShingles = self.shingles(content)
        indexedShingles = self.shingles(indexed_html)

        contentSketch, indexedSketch = self.sketch(contentShingles, indexedShingles)

        return self.jaccardSimilarity(contentSketch, indexedSketch)

    def shingles(self, content: str):
        index = 0
        sanitizedContent = re.sub(r'[.,!?;():\[\]{}\'\"]', '', content)
        words = sanitizedContent.split()
        shingles = []
        while index + self.shingle_size <= len(words):
            shingle = ' '.join(words[index:index + self.shingle_size])
            shingles.append(shingle)
            index += 1

        return shingles

    def sketch(self, contentShingles, indexedShingles):
        contentSketch = []
        indexedSketch = []
        for i in range(self.sketch_size):
            seed = i
            hashedContentShingles = self.hashShingle(contentShingles, seed)
            hashedIndexedShingles = self.hashShingle(indexedShingles, seed)

            minContent = self.min_shingle(hashedContentShingles)
            minIndexed = self.min_shingle(hashedIndexedShingles)

            contentSketch.append(minContent)
            indexedSketch.append(minIndexed)

        return contentSketch, indexedSketch

    def hashShingle(self, shingle, seed):
        hashed = set()
        for s in shingle:
            hashed_value = self.hasher(s, seed)
            hashed.add(hashed_value)
        return hashed

    def hasher(self, shing, seed):
        # Hashing the shingle into an integer value using SHA-256 and seed
        return int(hashlib.sha256((shing + str(seed)).encode()).hexdigest(), 16)

    def min_shingle(self, shingles):
        # Return the minimum hashed shingle
        return min(shingles)

    def jaccardSimilarity(self, contentSketch, indexedSketch):
        # Calculate Jaccard similarity between two sketches
        intersection = len(set(contentSketch).intersection(set(indexedSketch)))
        union = len(set(contentSketch).union(set(indexedSketch)))
        return intersection / union
