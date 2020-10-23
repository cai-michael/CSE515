from multiprocessing import Pool
import functools
import numpy as np
from task2 import *

# Retreive top 10 most similar gestures in non-increasing order of similarity
def retrive_similarity_matrix_row(gesture_file: str, vector_model: str, option: int):
    if option not in options:
        raise ValueError(f'Invalid option')
    return options[option][1](gesture_file, vector_model)

def getSingleRow(gesture_id, vector_model, option):
    # Refer to the global variable
    # Find similarity based on the metric
    similarities = retrive_similarity_matrix_row(gesture_id, vector_model, option)
    # Sort by name
    similarities.sort(key=lambda pair: int(pair[0]))
    # Only get similarity scores to add to the matrix
    modifiedSimilarities = [x[1] for x in similarities]
    return modifiedSimilarities

def createSimilarityMatrix(vector_model, option):
    # Create the similarity matrix
    print(f'Creating gesture-gesture similarity matrix based on {options[option][0]}...')
    filenames = util.get_files('./wrd_data', '.wrd')
    filenames = [x.split('.')[0] for x in filenames]
    filenames.sort(key=lambda x: int(x))
    similarityMatrix = np.empty([len(filenames), len(filenames)])

    # Multithread when finding each individual row of similarities
    findSingleRow = functools.partial(getSingleRow, vector_model=vector_model, option=option)
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
