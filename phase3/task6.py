import math
import os
import numpy as np
import general_util as util
from task2_util import *
from task3_util import load_vector, load_vectors, LSH
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

top_t_gestures = []
print(f'Top {t} most similar gestures:')
for index, (gesture_id, distance) in enumerate(top_t):
    print(f'{index + 1}.\t{gesture_id}\t(distance={distance})')
    top_t_gestures.append(gesture_id)
    
user_choice = 0
relevant_gestures = []
irrelevant_gestures = []
while user_choice != 4:
    print("Displaying Relevant Gestures")
    # Find t most similar gestures
    
    print('No. of buckets searched: ', no_buckets)
    print('No. of unique gestures considered: ', no_unique)
    print('Overall no. of gestures considered: ', overall_no)

    print(f'Top {t} most similar gestures:')
    for index, (gesture_id, distance) in enumerate(top_t):
        print(f'{index + 1}.\t{gesture_id}\t(distance={distance})')
    print("\nPick an option:\n1. Give Feedback\n2. Apply Probabilistic Revelance Feedback\n3. Classifier-Based Relevance Feedback\n4. Quit\n")
    user_choice = input()
    if user_choice == 1:
        print('Which gestures would you like to list as relevant? (e.g. 1, 249, 559, etc.):')
        relevant_gestures = input().replace(' ', '').split(',')
        print('Which gestures would you like to list as irrelevant? (e.g. 2, 258, 537, etc.):')
        irrelevant_gestures = input().replace(' ', '').split(',')
    elif user_choice == 2:
        print("Re-Running the Query with the new feedback...")
        probabilistic_relev(lsh, vector_model, query, top_t_gestures, relevant_gestures, irrelevant_gestures)
    elif user_choice == 3:
        print("Re-Running the Query with the new feedback...")
        #call function for task5
    elif user_choice == 4:
        print("Quit Chosen")
    else:
        print("Invalid User Choice!")
print("\nExiting.")
        
    
    