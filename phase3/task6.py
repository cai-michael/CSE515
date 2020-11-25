import math
import os
import numpy as np
import general_util as util
from task2_util import *
from task3_util import load_vector, load_vectors, LSH
from task4 import *
from graph_util import *

working_dir = os.getcwd()

L = int(input('Please enter the number of layers L: '))
k = int(input('Please enter the number of hashes per layer k: '))
vector_model = input('Please enter a vector model (TF/TF-IDF): ')
feedbackModel = input('Please choose a feedback system to utilize:\n1. Probabilistic Relevance Feedback\n2. Classifier-Based Relevance Feedback')

# Load vectors from vector_data folder
vectors, vector_ids = load_vectors(vector_model)

# Initialize LSH index structure
lsh = LSH(L, k, vectors, vector_ids)

gesture_id = input('Please enter a gesture id (e.g. 1, 249, 559, etc.): ')

t = int(input('Please enter t: '))

query = load_vector(vector_model, gesture_id)

# Find t most similar gestures
top_t, no_buckets, no_unique, overall_no = lsh.find_t_most_similar(query, t)
    
relevantResults = []
irrelevantResults = []
user_choice = 0
while user_choice != 3:
    print('No. of buckets searched: ', no_buckets)
    print('No. of unique gestures considered: ', no_unique)
    print('Overall no. of gestures considered: ', overall_no)

    print(f'Top {t} most similar gestures:')
    for index, (gesture_id, distance) in enumerate(top_t):
        print(f'{index + 1}.\t{gesture_id}\t(distance={distance})')

    print("\nPick an option:\n1. Give Feedback\n2. Re-run Query\n3. Quit\n")
    user_choice = int(input())
    if user_choice == 1:
        print("\nDo you want to specify the results as \n1. Relevant or \n2. Irrelevant")
        user_choice = int(input())
        string_choice = "relevant" if user_choice == 1 else "irrelevant"
        inputtedGestures = input(f"\nWhich gestures do you want to specify as {string_choice}?")
        feedbackGestures = inputtedGestures.replace(' ', '').split(',')
        if user_choice == 1:
            relevantResults.extend(feedbackGestures)
            relevantResults = list(set(relevantResults))
        else:
            irrelevantResults.extend(feedbackGestures)
            irrelevantResults = list(set(relevantResults))
    elif user_choice == 2:
        print("Re-Running the Query with the new feedback...")
        if feedbackModel == 1:
            newWeights = probabilistic_relev(lsh, vector_model, query, results, [results[relevant - 1]], [results[nonrelevant - 1], results[nonrelevant2 - 1]])
            top_t, no_buckets, no_unique, overall_no = lsh.find_t_most_similar(query, t, use_weights=False, weights=newWeights)
        else:
            
        
        relevantResults = []
        irrelevantResults = []
    elif user_choice == 3:
        print("Quit Chosen")
    else:
        print("Invalid User Choice!")
print("\nExiting.")
        
    
    