import math
import numpy as np

from task3_util import load_vectors

def probabilistic_relev(lsh, vector_model, query, results, relevant, nonrelevant):
    # print(results)
    print('Relevant: ')
    print(relevant)
    print('Nonrelevant: ')
    print(nonrelevant)

    vectors, gesture_ids = load_vectors(vector_model)
    threshold = .001  # minimum term frequency for a term to be counted as part of the document

    T = len(vectors[0])  # number of terms
    N = len(vectors)  # number of documents
    n = [0] * T  # document frequency array
    for vector in vectors:
        for i in range(len(vector)):
            n[i] += 1 if vector[i] > threshold else 0


    R = len(relevant)
    r = [0] * T  # relevant document frequency array
    for gesture_id in relevant:
        index = gesture_ids.index(gesture_id)
        vector = vectors[index]
        for i in range(len(vector)):
            r[i] += 1 if vector[i] > threshold else 0


    Z = len(nonrelevant)
    z = [0] * T  # nonrelevant document frequency array
    for gesture_id in nonrelevant:
        index = gesture_ids.index(gesture_id)
        vector = vectors[index]
        for i in range(len(vector)):
            z[i] += 1 if vector[i] > threshold else 0


    # print(n)
    # print(r)
    # print(z)

    weights = [0] * T
    for i in range(T):
        if r[i] == 0 and n[i] == 0 and z[i] == 0: # The term has never been seen before
            weights[i] = 0.0
        else:
            prob_relev = (r[i] + n[i] / N) / (R + 1.0)
            prob_nonrelev = (z[i] + n[i] / N) / (Z + 1.0)  # assumes nonrelevant documents are defined
            prob_nonrelev_paper = (n[i] - r[i] + n[i] / N) / (N - R + 1.0)  # assumes nonrelevant documents are all - relevant

            # print(prob_relev, prob_nonrelev)
            weights[i] = 1.0 if prob_relev == 1.0 else math.log((prob_relev * (1.0 - prob_nonrelev)) / (prob_nonrelev * (1.0 - prob_relev)))

    return weights
    
    """
    distances = []
    for gesture_id in results:
        index = lsh.vector_ids.index(gesture_id)
        vector = lsh.vectors[index]
        distances.append((gesture_id, lsh._distance(query, vector), lsh._weighted_distance(query, vector, weights)))

    distances.sort(key=lambda pair: pair[2])

    print(f'Probabilistic Relevance Feedback:')
    for index, (gesture_id, distance, weighted_distance) in enumerate(distances):
        print(f'{index + 1}.\t{gesture_id}\t(distance={distance})\t(weighted_distance={weighted_distance})')
    """


