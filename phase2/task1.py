import os
import math
import sys
from pathlib import Path
from typing import List
import general_util as util
import numpy as np
from task2 import load_vector, list_gesture_ids
from sklearn import decomposition

working_dir = os.getcwd()
# Make sure the output directory exists
if (not util.LATENT_SEMANTICS_FOLDER in os.listdir(working_dir)):
	os.mkdir(working_dir+util.SLASH+util.LATENT_SEMANTICS_FOLDER)

# Get the keys of all the words in our gesture-word dictionary
filename = Path('./vector_data') / f"tf_vectors_1.txt"
dict_word_to_vector_value = util.read_vector_txt(filename)
word_keys = list(dict_word_to_vector_value.keys())

# Get user's preferences
# Obtain the type of vector model
print('Specify the type of vector model, TF or TF-IDF:')
vector_model_input = input()
if vector_model_input not in ["TF","TF-IDF"]:
    print("Invalid vector model")
    print("vector_model_input")
    exit()

print('Specify the type of analysis, PCA SVD NMF or LDA:')
analysis_input = input()
if analysis_input not in ["PCA", "SVD", "NMF", "LDA"]:
    print("Invalid analysis type")
    exit()

print('Specify the number of latent semantics to extract: (e.g 1)')
top_k_input = int(input())
print("top k inputs is")
print(top_k_input)

def serialize_top_k_matrix(top_k_matrix):
    working_dir = os.getcwd()
    vector_model =  "tf" if vector_model_input == "TF" else "tfidf"
    output_file = open(working_dir+util.SLASH+util.LATENT_SEMANTICS_FOLDER+util.SLASH + f"{vector_model}_{analysis_input}_{top_k_input}.txt",'w')
    output_file2 = open(working_dir+util.SLASH+util.LATENT_SEMANTICS_FOLDER+util.SLASH + f"{vector_model}_{analysis_input}_{top_k_input}_unsorted.txt",'w')

    latent_semantic_index = 0

    for latent_semantic in top_k_matrix:
        # generate a list of (word, score) tuples, where the first element is the key in the dictionary,
        # and the second element is the score for that cell in the top_k matrix
        word_score_tuples = []
        for index in range(0, top_k_matrix.shape[1]):
            word_score_tuples.append((word_keys[index], latent_semantic[index]))
        
        for word_score_pair in word_score_tuples:
            output_file2.write(str((latent_semantic_index, word_score_pair)) + '\n')
        
        # sort the list in descending order
        word_score_tuples.sort(key=lambda pair: pair[1], reverse=True)
        # write to output_file, with key of the tuple being the index of the top k latent component (e.g. 1 or 2)
        for word_score_pair in word_score_tuples:
            output_file.write(str((latent_semantic_index, word_score_pair)) + '\n')
        latent_semantic_index +=1

    output_file.close()

def get_top_k_latent_semantics(k, model, gesture_word_matrix):
    if model == "PCA":
        model = decomposition.PCA(n_components=top_k_input)
    if model == "SVD":
        model = decomposition.TruncatedSVD(n_components=top_k_input)
    if model == "NMF":
        model = decomposition.NMF(n_components=top_k_input)
    if model == "LDA":
        model = decomposition.LatentDirichletAllocation(n_components=top_k_input)

    model.fit(gesture_word_matrix)

    # take the top-k latent semantics
    top_k_matrix = model.components_
    return top_k_matrix

gesture_word_matrix = []
for id in list_gesture_ids():
    gesture_word_matrix.append(load_vector(id, vector_model_input))
    
gesture_word_matrix = np.array(gesture_word_matrix)
top_k_matrix = get_top_k_latent_semantics(top_k_input, analysis_input, gesture_word_matrix)
serialize_top_k_matrix(top_k_matrix)
