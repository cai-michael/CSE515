import math
import os
import numpy as np
import general_util as util
from task2_util import *
from task3_util import load_vector, load_vectors, LSH
from task4 import *
from graph_util import *
from task4 import probabilistic_relev

working_dir = os.getcwd()

# Obtain querying inputs
L = int(input('Please enter the number of layers L: '))
k = int(input('Please enter the number of hashes per layer k: '))
vector_model = input('Please enter a vector model (TF/TF-IDF): ').upper()
feedback_model = int(input("Please pick which feedback model you would like to use\n1. Probabilistic Relevance Feedback\n2. Classifier-based Relevance Feedback\n"))

if feedback_model == 2:
    print('\nLoading Similarity Matrix and Graph...\n')
    data_files, similarity_matrix = util.read_similarity_matrix(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt')
    similarity_graph = util.read_similarity_graph(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt')

# Load vectors from vector_data folder
vectors, vector_ids = load_vectors(vector_model)

# Initialize LSH index structure
lsh = LSH(L, k, vectors, vector_ids)

gesture_id = input('Please enter a gesture id (e.g. 1, 249, 559, etc.): ')

t = int(input('Please enter t: '))

query = load_vector(vector_model, gesture_id)

# Find t most similar gestures
top_t, no_buckets, no_unique, overall_no = lsh.find_t_most_similar(query, t)

print('No. of buckets searched: ', no_buckets)
print('No. of unique gestures considered: ', no_unique)
print('Overall no. of gestures considered: ', overall_no)

print(f'Top {t} most similar gestures:')
for index, (gesture_id, distance) in enumerate(top_t):
    print(f'{index + 1}.\t{gesture_id}\t(distance={distance})')
    
relevant_gestures = []
irrelevant_gestures = []
current_weights = None
user_choice = 0
while user_choice != 3:
    print("\nPick an option:\n1. Give Feedback\n2. Apply Revelance Feedback\n3. Quit\n")
    user_choice = int(input())
    if user_choice == 1:
        print("\nDo you want to specify the results as \n1. Relevant\n2. Irrelevant\n")
        user_choice = int(input())
        string_choice = "relevant" if user_choice == 1 else "irrelevant"
        inputtedGestures = input(f"\nWhich gestures do you want to specify as {string_choice}?\n")
        feedbackGestures = inputtedGestures.replace(' ', '').split(',')
        if user_choice == 1:
            relevant_gestures.extend(feedbackGestures)
            relevant_gestures = list(set(relevant_gestures))
        else:
            irrelevant_gestures.extend(feedbackGestures)
            irrelevant_gestures = list(set(irrelevant_gestures))
    elif user_choice == 2:
        # The user picked the probabilistic based relevance feedback system
        if feedback_model == 1:
            print("Re-Running the Query with Probabilistic Relevance Feedback")
            current_weights = probabilistic_relev(lsh, vector_model, query, relevant_gestures, irrelevant_gestures, initialWeights=current_weights)
            
            distances = []
            for gesture_id, _ in top_t:
                index = lsh.vector_ids.index(gesture_id)
                vector = lsh.vectors[index]
                distances.append((gesture_id, lsh._distance(query, vector), lsh._weighted_distance(query, vector, current_weights)))

            distances.sort(key=lambda pair: pair[2])

            print(f'Probabilistic Relevance Feedback:')
            for index, (gesture_id, distance, weighted_distance) in enumerate(distances):
                print(f'{index + 1}.\t{gesture_id}\t(distance={distance})\t(weighted_distance={weighted_distance})')
        
        # The user picked the classifier based relevance feedback system
        else:
            print("Re-Running the Query with Classifier-Based Relevance Feedback")

        # Clean up between relevance feedback
        relevant_gestures = []
        irrelevant_gestures = []

    elif user_choice == 3:
        print("Quit Chosen")
    else:
        print("Invalid User Choice!")
print("\nExiting.")
    