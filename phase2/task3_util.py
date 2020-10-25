import numpy as np
from task2 import *

# Retreive top 10 most similar gestures in non-increasing order of similarity
def retrive_similarity_matrix_row(gesture_file: str, vector_model: str, option: int, top_k_input: int):
    if option not in options:
        raise ValueError(f'Invalid option')
    return options[option][1](gesture_file, vector_model, top_k_input)

def createSimilarityMatrix(vector_model, option, top_k_input):
    # Create the similarity matrix
    print(f'Creating gesture-gesture similarity matrix based on {options[option][0]}...')
    filenames = util.get_files('./wrd_data', '.wrd')
    filenames = [x.split('.')[0] for x in filenames]
    filenames.sort(key=lambda x: int(x))
    similarityMatrix = np.empty([len(filenames), len(filenames)])
    for index, gesture_id in enumerate(filenames):
        similarities = retrive_similarity_matrix_row(gesture_id, vector_model, option, top_k_input)
        # Sort by name
        similarities.sort(key=lambda pair: int(pair[0]))
        modifiedSimilarities = [x[1] for x in similarities]
        similarityMatrix[index] = modifiedSimilarities
    
    # Convert distances to similarity if they are distances
    if option >= 6:
        # Normalize the matrix and subtract from 1 to find similarity
        maxValue = np.max(similarityMatrix)
        conversion = lambda d: 1 - (d / maxValue)
        similarityMatrix = conversion(similarityMatrix)

    return similarityMatrix, filenames
