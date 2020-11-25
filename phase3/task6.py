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

L = int(input('Please enter the number of layers L: '))
k = int(input('Please enter the number of hashes per layer k: '))
vector_model = input('Please enter a vector model (TF/TF-IDF): ')

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
while user_choice != 4:
    print("\nPick an option:\n1. Give Feedback\n2. Apply Probabilistic Revelance Feedback\n3. Classifier-Based Relevance Feedback\n4. Quit\n")
    user_choice = int(input())
    if user_choice == 1:
        print("\nDo you want to specify the results as \n1. Relevant\n2. Irrelevant")
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

    elif user_choice == 3:
        print("Re-Running the Query with Classifier-Based Relevance Feedback")
    elif user_choice == 4:
        print("Quit Chosen")
    else:
        print("Invalid User Choice!")
print("\nExiting.")
        
    
    