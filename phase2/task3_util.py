from multiprocessing import Pool
import functools
import numpy as np
from task2 import *

# Retreive top 10 most similar gestures in non-increasing order of similarity
def retrive_similarity_matrix_row(gesture_file: str, vector_model: str, option: int, top_k_input: int):
    if option not in options:
        raise ValueError(f'Invalid option')
    return options[option][1](gesture_file, vector_model, top_k_input)

def getSingleRow(gesture_id, vector_model, option, top_k_input):
    # Refer to the global variable
    # Find similarity based on the metric
    similarities = retrive_similarity_matrix_row(gesture_id, vector_model, option, top_k_input)
    # Sort by name
    similarities.sort(key=lambda pair: int(pair[0]))
    # Only get similarity scores to add to the matrix
    modifiedSimilarities = [x[1] for x in similarities]
    return modifiedSimilarities

def createSimilarityMatrix(vector_model, option, top_k_input):
    # Create the similarity matrix
    print(f'Creating gesture-gesture similarity matrix based on {options[option][0]}...')
    filenames = util.get_files('./wrd_data', '.wrd')
    filenames = [x.split('.')[0] for x in filenames]
    filenames.sort(key=lambda x: int(x))
    similarityMatrix = np.empty([len(filenames), len(filenames)])

    # Multithread when finding each individual row of similarities
    findSingleRow = functools.partial(getSingleRow, vector_model=vector_model, option=option, top_k_input=top_k_input)
    with Pool() as p:
        results = p.map(findSingleRow, filenames)
    
    for index, row in enumerate(results):
        similarityMatrix[index] = row
    
    # Convert distances to similarity if they are distances
    if option >= 6:
        # Normalize the matrix and subtract from 1 to find similarity
        maxValue = np.max(similarityMatrix)
        conversion = lambda d: 1 - (d / maxValue)
        similarityMatrix = conversion(similarityMatrix)

    return similarityMatrix, filenames

def rescale(data, new_min=0, new_max=1):
    return (data - data.min()) / (data.max() - data.min()) * (new_max - new_min) + new_min