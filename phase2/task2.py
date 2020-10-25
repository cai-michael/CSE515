import sys
from pathlib import Path
from typing import List
import general_util as util
import task0_util
import numpy as np

# Utils
def list_gesture_ids():
    filenames = util.get_files('./wrd_data', '.wrd')
    gesture_ids = [filename.split('.')[0] for filename in filenames]
    return gesture_ids

def load_vector(gesture_id: str, vector_model: str) -> List[float]:
    if vector_model != 'TF' and vector_model != 'TF-IDF':
        raise ValueError('Invalid vector model')
    model = 'tf' if vector_model == 'TF' else 'tfidf'
    filepath = Path('./vector_data') / f'{model}_vectors_{gesture_id}.txt'
    vector = util.read_vector_txt_to_list(filepath)
    return vector

def load_latent_component_feature_matrix(vector_model, top_k_number, analysis_type):
    if vector_model != 'TF' and vector_model != 'TF-IDF':
        raise ValueError('Invalid vector model')
    model = 'tf' if vector_model == 'TF' else 'tfidf'
    # example tf_PCA_3.txt, means get the PCA analysis for top 3 components on the gesture word TF matrix
    filepath = Path('./latent_semantics_data') / f'{model}_{analysis_type}_{top_k_number}_unsorted.txt'
    #geature = util.read_vector_txt_to_list(filepath)
    lines = util.read_nonempty_lines(filepath)

    
    component_feature_matrix = []
    for index in range(0, top_k_number):
        component_feature_vector = []
        for line in lines:
            (latent_component_index, (word_key, score)) = eval(line)
            if latent_component_index == index:
                component_feature_vector.append(score)
            
        component_feature_matrix.append(component_feature_vector)
    
    component_feature_matrix = np.array(component_feature_matrix)
    return component_feature_matrix


# Option 1 (Dot product similarity)
# Compute dot product of two vectors
def dot_product_sim(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError('Vector lengths do not match')
    dot_product = sum([c1 * c2 for c1, c2 in zip(v1, v2)])
    return dot_product

def cosine_sim(a, b):
    from numpy import dot
    from numpy.linalg import norm
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim

def top_k_latent_semantic_sim(gesture_id1: str, gesture_id2: str, vector_model, latent_component_vector) -> float:
    vector1 = np.array(load_vector(gesture_id1, vector_model))
    vector1 = vector1.dot(latent_component_vector.T)
    vector2 = np.array(load_vector(gesture_id2, vector_model))
    vector2 = vector2.dot(latent_component_vector.T)
    similarity = cosine_sim(vector1, vector2)
    return similarity
    
def dot_product_gesture_sim(gesture_id1: str, gesture_id2: str, vector_model: str) -> float:
    vector1 = load_vector(gesture_id1, vector_model)
    vector2 = load_vector(gesture_id2, vector_model)
    similarity = dot_product_sim(vector1, vector2)
    return similarity


def option1(gesture_id, vector_model):
    gesture_ids = list_gesture_ids()
    similarities = [(gesture_id2, dot_product_gesture_sim(gesture_id, gesture_id2, vector_model)) for gesture_id2 in gesture_ids]
    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities


# Option 2 (PCA)
def option2(gesture_id, vector_model, top_k_input):
    gesture_ids = list_gesture_ids()
    latent_component_vector = load_latent_component_feature_matrix(vector_model, top_k_input, "PCA")
    similarities = [(gesture_id2, top_k_latent_semantic_sim(gesture_id, gesture_id2, vector_model, latent_component_vector)) for gesture_id2 in gesture_ids]
    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities


# Option 3 (SVD)
def option3(gesture_id, vector_model, top_k_input):
    gesture_ids = list_gesture_ids()
    latent_component_vector = load_latent_component_feature_matrix(vector_model, top_k_input, "SVD")
    similarities = [(gesture_id2, top_k_latent_semantic_sim(gesture_id, gesture_id2, vector_model, latent_component_vector)) for gesture_id2 in gesture_ids]
    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities


# Option 4 (NMF)
def option4(gesture_id, vector_model, top_k_input):
    gesture_ids = list_gesture_ids()
    latent_component_vector = load_latent_component_feature_matrix(vector_model, top_k_input, "NMF")
    similarities = [(gesture_id2, top_k_latent_semantic_sim(gesture_id, gesture_id2, vector_model, latent_component_vector)) for gesture_id2 in gesture_ids]
    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities

# Option 5 (LDA)
def option5(gesture_id, vector_model, top_k_input):
    gesture_ids = list_gesture_ids()
    latent_component_vector = load_latent_component_feature_matrix(vector_model, top_k_input, "LDA")
    similarities = [(gesture_id2, top_k_latent_semantic_sim(gesture_id, gesture_id2, vector_model, latent_component_vector)) for gesture_id2 in gesture_ids]
    similarities.sort(key=lambda pair: pair[1], reverse=True)
    return similarities

# Option 6 (Edit distance)
"""
Utilizes a symmetric cost function based on the midpoints of each band. 
The cost of replacing is the distance from the midpoints from each band.
"""
#gives the midpoint of the gaussian band to which x belongs
def get_band_midpoint(bands, x):
	return (util.GAUSSIAN_BANDS[x]+util.GAUSSIAN_BANDS[x+1])/2.0

def cost_insert(val):
    midpoint = get_band_midpoint(util.GAUSSIAN_BANDS, val)
    return abs(midpoint)


def cost_delete(val):
    midpoint = get_band_midpoint(util.GAUSSIAN_BANDS, val)
    return abs(midpoint)

# Cost of replacing val1 with val2
def cost_replace(val1, val2):
    midpoint1 = get_band_midpoint(util.GAUSSIAN_BANDS, val1)
    midpoint2 = get_band_midpoint(util.GAUSSIAN_BANDS, val2)
    return abs(midpoint1 - midpoint2)

"""
Recursively determines the edit distance between two time series P and Q.
i - current prefix index of P
j - current prefix index of Q
D - the memoization matrix where [0][0] is the start of both strings and [i][j] are the ends
"""
def edit_dist_aux(P, Q, i, j, D):
    # Case 1: Accounting for illegal edges
    if i == -1 or j == -1:
        return float('inf')
    # Case 2: The minimum distance to this prefix is already calculated
    if D[i][j] != -1:
        return D[i][j]
    # Case 3: There is a match in the strings
    if i > 0 and j > 0 and P[i - 1] == Q[j - 1]:
        dist = edit_dist_aux(P, Q, i - 1, j - 1, D)
        D[i][j] = dist
        return dist
    # Case 4: There is a mismatch
    dist = min(
        (cost_insert(Q[j - 1]) if j > 0 else float('inf')) + edit_dist_aux(P, Q, i, j - 1, D),
        (cost_delete(P[i - 1]) if i > 0 else float('inf')) + edit_dist_aux(P, Q, i - 1, j, D),
        (cost_replace(P[i - 1], Q[j - 1]) if i > 0 and j > 0 else float('inf')) + edit_dist_aux(P, Q, i - 1, j - 1, D)
    )
    D[i][j] = dist
    return dist


def get_memo(N, M):
    D = []
    for _ in range(N + 1):
        D.append([-1] * (M + 1))
    D[0][0] = 0
    return D


# Get edit distance between two wrd sequences
def edit_distance(P, Q):
    N = len(P)
    M = len(Q)
    D = get_memo(N, M)
    dist = edit_dist_aux(P, Q, N, M, D)
    return dist


# Outputs overall edit distance betweeng gesture1 and gesture2
# Edit distances are computed for each combination of component and sensor_id.
# These distances are then added up to produce a total distance.
# gesture1 and gesture2 are the names of the wrd files without the .wrd
# extension.
def gesture_edit_distance(gesture1, gesture2):
    distances = []
    wrds1 = util.read_wrd_general(Path(util.WRD_FOLDER) / f'{gesture1}.wrd')
    wrds2 = util.read_wrd_general(Path(util.WRD_FOLDER) / f'{gesture2}.wrd')
    for component in util.COMPONENTS:
        for sensor_id in range(20):
            P = [t[1] for t in wrds1[component][sensor_id]['series']]
            Q = [t[1] for t in wrds2[component][sensor_id]['series']]
            distance = edit_distance(P, Q)
            distances.append(distance)
    total_distance = sum(distances)
    return total_distance


def option6(gesture_file, vector_model, top_k_input=None):
    filenames = util.get_files('./wrd_data', '.wrd')
    distances = []
    for filename in filenames:
        gesture_id = filename.split('.')[0]
        distance = gesture_edit_distance(gesture_file, gesture_id)
        distances.append((gesture_id, distance))
    distances.sort(key=lambda pair: pair[1])
    return distances


# Option 7 (DTW)
# Utilizes the O(N * M) solution to determine the least distance in dynamic time warping
def dtw_aux(P, Q, N, M, D):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            D[i][j] = abs(P[i - 1] - Q[j - 1]) + min(D[i-1][j-1], D[i][j-1], D[i-1][j]) 
    dist = D[N][M]
    return dist

# Initialize Memoization Matrix with inf on the edges and None's in the center.
def get_dtw_memo(P, Q, N, M):
    D = []
    for i in range(N + 1):
        D.append([None] * (M + 1))
    for i in range(1, N + 1):
        D[i][0] = float('inf')
    for j in range(1, M + 1):
        D[0][j] = float('inf')
    D[0][0] = 0
    return D


# DTW from timeseries P to timeseries Q
def dtw_distance(P, Q):
    N = len(P)
    M = len(Q)
    D = get_dtw_memo(P, Q, N, M)
    dist = dtw_aux(P, Q, N, M, D)
    return dist


def gesture_dtw_distance(gesture1, gesture2):
    distances = []
    wrds1 = util.read_wrd_general(Path(util.WRD_FOLDER) / f'{gesture1}.wrd')
    wrds2 = util.read_wrd_general(Path(util.WRD_FOLDER) / f'{gesture2}.wrd')
    for component in util.COMPONENTS:
        for sensor_id in range(20):
            P = [t[0] for t in wrds1[component][sensor_id]['series']]
            Q = [t[0] for t in wrds2[component][sensor_id]['series']]
            distance = dtw_distance(P, Q)
            distances.append(distance)
    return sum(distances)


def option7(gesture_file, vector_model, top_k_input=None):
    filenames = util.get_files('./wrd_data', '.wrd')
    distances = []
    for filename in filenames:
        gesture_id = filename.split('.')[0]
        distance = gesture_dtw_distance(gesture_file, gesture_id)
        distances.append((gesture_id, distance))
    distances.sort(key=lambda pair: pair[1])
    return distances


# Options map mapping option number to a tuple
# (<option_name>, <option_func>, <score_metric>),
# where <option_name> is the name of the option,
# <option_func> is the actual function that retreives
# the top 10 most similiar gestures, and <score_metric>
# is whether vectors were compared using similarity or distance
options = {
    1: ('Dot product similarity', option1, 'similarity'),
    2: ('PCA', option2, 'similarity'),
    3: ('SVD', option3, 'similarity'),
    4: ('NMF', option4, 'similarity'),
    5: ('LDA', option5, 'similarity'),
    6: ('Edit distance', option6, 'distance'),
    7: ('DTW distance', option7, 'distance')
}


# Retreive top 10 most similar gestures in non-increasing order of similarity
def find_10_most_similar_gestures(gesture_file: str, vector_model: str, option: int):
    if option not in options:
        raise ValueError(f'Invalid option')
    if option in [2,3,4,5]:
        top_k_input = int(input('How many top-k components did you specify during Task 1?  (e.g. 1, 2, etc.): '))
    return options[option][1](gesture_file, vector_model, top_k_input)[0:10]


# Main
if __name__ == '__main__':
    # Load User Settings
    util.load_user_settings()

    # Load arguments
    gesture_file = input('Gesture file (e.g. 1, 249, 559, etc.): ')

    # List options
    print('Options:')
    for option_number, (option_name, _, _) in options.items():
        print(f'{option_number}. {option_name}')

    option = int(input('Please select an option: '))
    while option not in options:
        print('Invalid option. Please try again.')
        option = int(input('Please select an option: '))

    vector_model = None

    if option < 6:
        vector_model = input('Please select a vector model (TF/TF-IDF): ').upper()
        while vector_model not in { 'TF', 'TF-IDF' }:
            print('Invalid vector model. Please try again.')
            vector_model = input('Please select a vector model (TF/TF-IDF): ')

    # Retreive top 10
    print(f'Retreiving top 10 most similar gestures based on {options[option][0]}...')
    top10 = find_10_most_similar_gestures(gesture_file, vector_model, option)

    # Display results
    print('10 most similar gestures:')

    for index, (gesture, score) in enumerate(top10):
        print(f'{index + 1}.\t{gesture}\t({options[option][2]}={score})')
