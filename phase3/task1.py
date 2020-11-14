import general_util as util
import os
import numpy as np
from graph_util import *

working_dir = os.getcwd()
util.load_user_settings()

# Make sure the output directory exists
util.check_folder(working_dir, util.GRAPH_FOLDER)

data_files, similarity_matrix = util.read_similarity_matrix(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt')



# Create similarity graph
print('Please specify a desired degree k for the similarity graph:')
util.DEGREE = int(input())

util.save_user_settings()

similarity_graph = create_similarity_graph(util.DEGREE, similarity_matrix, data_files)

output_file = open(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt','w')
for gesture in similarity_graph:
	output_file.write(gesture + ': ')
	output_file.write(str(similarity_graph[gesture]).replace(' ','').replace("'",'')[1:-1]+'\n')
output_file.close()

transition_matrix = create_transition_matrix(similarity_graph)

print('Please specify the number m of dominant gestures to retrieve:')
num_dominant_gestures = int(input())
num_dominant_gestures = min(num_dominant_gestures, len(data_files))



# Request seed gestures
print('Please specify the seed gestures for Personalized Page Rank: (e.g. "1, 277, 63")')
seed_gestures = input().replace(' ','').split(',')

# Discard invalid seeds
seed_gestures = list(filter(lambda a : a in data_files, seed_gestures))
seed_gestures = list(set(seed_gestures)) # remove redundancies



# Compute dominant gestures
init_vector = np.zeros((len(data_files), 1))
for gesture in seed_gestures:
	init_vector[data_files.index(gesture), 0] = 1.0/len(seed_gestures)

ppr = personalized_page_rank(transition_matrix, init_vector, 0.1)

dominant_gestures = ppr.transpose().tolist()[0]
dominant_gestures = sorted(range(len(dominant_gestures)), reverse=True, key=lambda a : dominant_gestures[a])
dominant_gestures = [data_files[a] for a in dominant_gestures]
dominant_gestures = dominant_gestures[0:num_dominant_gestures]

print('\nFound the following dominant gestures:')
for g in dominant_gestures:
	print(g)



# Visualize dominant gestures


