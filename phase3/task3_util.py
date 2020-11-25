from pathlib import Path
import general_util as util

from typing import List, Any
import numpy as np
import random
import math


def load_vector(vector_model: str, gesture_id: str):
    if vector_model not in {'TF', 'TF-IDF'}:
        raise ValueError('Invalid vector model')
    prefix = 'tf' if vector_model == 'TF' else 'tfidf'
    filename = f'{prefix}_vector_{gesture_id}.txt'
    filepath = Path(util.VECTOR_FOLDER) / filename
    vector = util.read_vector_txt_to_list(filepath)
    return vector


# Load vectors of the specified vector model
# and the gesture ids associated with each vector
def load_vectors(vector_model: str):
    print('Loading gesture vectors...')
    vectors = []
    gesture_ids = []
    if vector_model not in {'TF', 'TF-IDF'}:
        raise ValueError('Invalid vector model')
    model = 'tf' if vector_model == 'TF' else 'tfidf'
    filenames = util.get_files(util.VECTOR_FOLDER, '.txt')
    for filename in filenames:
        prefix, _, gesture_id = filename.split('.')[0].split('_', maxsplit=2)
        if prefix == model:
            vector = load_vector(vector_model, gesture_id)
            vectors.append(vector)
            gesture_ids.append(gesture_id)
    return vectors, gesture_ids


# In-memory index structure based on LSH
class LSH:

    def __init__(
        self,
        L: int,
        k: int,
        vectors: List[float],
        vector_ids: List[Any]=None,
        w=0.01,   # Length of window
        s=2       # s-norm distance
    ):
        print('Initializing LSH index structure...')
        self.L = L
        self.k = k
        self.vectors = vectors
        self.vector_ids = vector_ids or vectors
        self.w = w
        self.s = s

        self._init_layers()
        self._init_buckets()

        print('Initialized LSH index structure.')

    # Sample L * k hash functions from H
    # self.g[i] returns the ith layer
    def _init_layers(self):
        print(f'Initializing {self.L} layers...')
        self.g = []
        for _ in range(self.L):
            layer = []
            for _ in range(self.k):
                h = self._generate_hash_function()
                layer.append(h)
            self.g.append(layer)

    # Sample hash function from Ls family
    def _generate_hash_function(self):
        dim = len(self.vectors[0])                    # dimension of vector space
        w = self.w                                    # length of window
        p = np.random.normal(0, 1, dim)               # scaled projection vector
        b = w * random.random()                       # [0, w)
        h = lambda x: math.floor((p.dot(x) + b) / w)
        return h

    # Hash a vector using the specified layer
    def _hash_vector(self, vector: List[float], layer_id: int) -> tuple:
        layer = self.g[layer_id]
        bucket_id = tuple([h(vector) for h in layer])
        return bucket_id

    # Init buckets and add vectors to buckets
    def _init_buckets(self):
        print('Initializing buckets...')
        # Create L hash tables, one for each layer
        self.tables = [{} for _ in self.g]
        for i, vector in enumerate(self.vectors):
            for j, table in enumerate(self.tables):
                bucket_id = self._hash_vector(vector, j)
                if bucket_id not in table:
                    table[bucket_id] = []   # Create new bucket
                table[bucket_id].append(i)  # Add vector index to bucket

    # Compute Ls distance between two vectors v1 and v2
    def _distance(self, v1: List[float], v2: List[float]) -> float:
        s = self.s
        distance = sum([abs(c1 - c2) ** s for c1, c2 in zip(v1, v2)]) ** (1 / s)
        return distance

    def _weighted_distance(self, v1: List[float], v2: List[float], weights: List[float]) -> float:
        s = self.s
        distance = 0.0
        for i in range(len(v1)):
            distance += (abs(v1[i] - v2[i]) * weights[i]) ** s
        distance = distance ** (1 / s)
        return distance

    # Find top t vectors most similar to query vector
    def find_t_most_similar(self, query: List[float], t: int):
        no_buckets_searched = 0
        overall_no_vectors_considered = 0
        candidates = set()
        # Search all layers
        print('Searching for candidates...')
        for i, table in enumerate(self.tables):
            bucket_id = self._hash_vector(query, i)
            bucket = table.get(bucket_id, None)
            if bucket:
                no_buckets_searched += 1
                overall_no_vectors_considered += len(bucket)
                candidates.update(bucket)
        candidates = list(candidates)
        no_unique_vectors_considered = len(candidates)
        print('Computing distances...')
        distances = [(self.vector_ids[c], self._distance(query, self.vectors[c])) for c in candidates]
        distances.sort(key=lambda pair: pair[1])
        top_t = distances if len(distances) < t else distances[:t]
        return top_t, no_buckets_searched, no_unique_vectors_considered, overall_no_vectors_considered
