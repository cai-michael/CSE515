import general_util as util
from graph_util import *
import os
import operator
import numpy as np

# remove irrelevant gestures from similarity_graph
def update_similarity_graph(similarity_graph, irrelevant_gestures):
	for gesture in irrelevant_gestures:
		for g in similarity_graph:
			if gesture in similarity_graph[g]:
				similarity_graph[g].pop(similarity_graph[g].index(gesture))

def create_init_vector(data_files, seed_gestures):
	init_vector = np.zeros((len(data_files), 1))
	for gesture in seed_gestures:
		init_vector[data_files.index(gesture), 0] = 1.0/len(seed_gestures)
	return init_vector

# Compute dominant gestures
def get_sorted_gesture_scores(similarity_graph, transition_matrix, init_vector):
	ppr = personalized_page_rank(transition_matrix, init_vector, 0.1)
	gesture_score_dict = {}
	gesture_index_in_graph = list(similarity_graph.keys())
	dominant_gestures = ppr.transpose().tolist()[0]
	for index in range(len(dominant_gestures)):
		score = dominant_gestures[index] # the score from PPR
		gesture_name = gesture_index_in_graph[index]
		if gesture_score_dict.get(gesture_name): # check if this gesture is in the dict
			if gesture_score_dict[gesture_name] < score:
				gesture_score_dict[gesture_name] = score
		else:
			gesture_score_dict[gesture_name] = score
	return dict(sorted(gesture_score_dict.items(), key=operator.itemgetter(1), reverse=True))



# this is the one that should be used in task6
# will permanently alter similarity_graph
def classifier_relev(data_files, similarity_graph, top_t_gestures, relevant, irrelevant):
	update_similarity_graph(similarity_graph, irrelevant)
	
	# Build transition matrix
	transition_matrix = create_transition_matrix(similarity_graph)

	# initialize seed gestures with the relevant gestures
	seed_gestures = list(filter(lambda a : a in data_files, relevant))
	seed_gestures = list(set(seed_gestures)) # remove redundancies
	init_vector = create_init_vector(data_files, seed_gestures)
	
	return get_sorted_gesture_scores(similarity_graph, transition_matrix, init_vector)



# runs classifier_relev from scratch (i.e. the saved similarity matrix file)
def oneshot_classifier_relev(top_t_gestures, relevant, irrelevant):
	working_dir = os.getcwd()

	#Personalized Page Rank
	# Retrieve similiarity matrix, graph, and data files to use in calculation
	data_files, similarity_matrix = util.read_similarity_matrix(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt')

	similarity_graph = util.read_similarity_graph(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt')

	sorted_gesture_scores = classifier_relev(data_files, similarity_graph, top_t_gestures, relevant, irrelevant)
	
	order = 0
	print(f'Classifier-based relevance feedback:')
	for gesture_id, score in sorted_gesture_scores.items():
		if gesture_id in top_t_gestures:
			print(f'{order + 1}.\t{gesture_id}\t(score={score})')
			order += 1


