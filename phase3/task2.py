import math
import os
import numpy as np
import general_util as util
from task2_util import *
from graph_util import *

working_dir = os.getcwd()

print('Which classifier would you like to use?')
print('1: k nearest neighbors')
print('2: personalized page rank')
print('3: decision trees')

# Get user input 
classifier = input()
while(not classifier in ['1', '2', '3']):
	print('Unrecognized classifier.')
	classifier = input()
classifier = int(classifier)


# list of the names of all gestures in the database
data_files = util.get_files(util.WRD_FOLDER,'.wrd')
data_files = [a[0:-4] for a in data_files] # strip file extension

#load tfidf data by default
vector_data = {f : util.read_vector(util.VECTOR_FOLDER+util.SLASH+'tfidf_vector_'+f+'.txt') for f in data_files}


print('\nPlease specify the number of distinct labels for classification:')
labeled_gestures = {} # dict of form {gesture name : label}
classes = {label : [] for label in range(int(input()))} # dict of form {label : [gesture names]}
print('\nTo specify the gestures in a label, use a comma-separated list. (e.g. "1, 3, 8")')
print('You can also specify ranges using a colon. (e.g. "5:9")')
sortedDataFiles = util.sortFileNames(data_files)
print('Select files from: ' + data_files_to_pretty_string(sortedDataFiles) + '\n')

for label in classes:
	print('Please specify just the gestures for label '+str(label)+'.')
	command = input().replace(' ','').split(',')
	for word in command:
		if(':' in word): # specify a range
			word = word.split(':')
			firstWordIndex = sortedDataFiles.index(word[0])
			secondWordIndex = sortedDataFiles.index(word[1])
			rangeOfFiles = sortedDataFiles[firstWordIndex:secondWordIndex + 1]
			for w in rangeOfFiles:
				labeled_gestures[w] = label
				classes[label].append(w)
		elif(word in data_files):
			labeled_gestures[word] = label
			classes[label].append(word)
#print(labeled_gestures)
#print(classes)

all_gestures = set(data_files)
# Identify the unclassified gestures
unclassified_gestures = set(data_files)
unclassified_gestures = unclassified_gestures.difference(set(labeled_gestures.keys()))
unclassified_gestures = list(unclassified_gestures)


# Each classification method should add unclassified_gestures to the lists in the 'classes' dictionary
if(classifier == 1):
	print('Please select the degree k for nearest neighbors:')
	k = int(input())
	
	print('Classifying gestures using '+str(k)+' nearest neighbors...')
	
	labeled_gesture_matrix = [list(vector_data[f].values()) for f in labeled_gestures]
	labeled_gesture_matrix = np.matrix(labeled_gesture_matrix)
	num_labeled_gestures, num_dimensions = np.shape(labeled_gesture_matrix)
	
	labeled_gesture_names = list(labeled_gestures.keys())
	labeled_gesture_names = {labeled_gesture_names[i] : i for i in range(len(labeled_gesture_names))}
	
	for g in all_gestures:
		one_vector = np.ones((num_labeled_gestures,1))
		gesture_vector = np.matrix(list(vector_data[g].values()))
		distances = np.matmul(one_vector, gesture_vector)
		
		distances = np.subtract(distances, labeled_gesture_matrix)
		distances = np.multiply(distances, distances)
		
		one_vector = np.ones((num_dimensions,1))
		distances = np.matmul(distances, one_vector)
		distances = distances.transpose().tolist()[0]
		distances = list(map(math.sqrt, distances))
		
		ranking = sorted(labeled_gestures.keys(), key=lambda a : distances[labeled_gesture_names[a]])
		ranking = ranking[0:k]
		ranking = [labeled_gestures[f] for f in ranking] # get labels
		final_vote = majority_vote(ranking)
		classes[majority_vote(ranking)].append(g)

elif(classifier == 2):
	print('Classifying gestures using personalized page rank...')
	similarity_graph = util.read_similarity_graph(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt')
	transition_matrix = create_transition_matrix(similarity_graph)

	# a dictionary to track the highest PPR score and class label for a gesture
	gesture_score_dict = {}
	gesture_index_in_graph = list(similarity_graph.keys())
	for label in classes:
		labeled_gestures_in_class = classes[label]

		# Init seed gestures as the labeled gestures
		init_vector = np.zeros((len(data_files), 1))
		for gesture in labeled_gestures_in_class:
			init_vector[gesture_index_in_graph.index(gesture), 0] = 1.0/len(labeled_gestures_in_class)
	
		ppr = personalized_page_rank(transition_matrix, init_vector, 0.1)
		dominant_gestures = ppr.transpose().tolist()[0]
		for index in range(len(dominant_gestures)):
			score = dominant_gestures[index] # the score from PPR
			gesture_name = gesture_index_in_graph[index]
			if gesture_score_dict.get(gesture_name): # check if this gesture is in the dict
				if gesture_score_dict[gesture_name][0] < score:
					gesture_score_dict[gesture_name] = (score, label)
			else:
				gesture_score_dict[gesture_name] = (score, label)
	# print(gesture_score_dict) prints the breakdown of scores for a given gesture using PPR
	for gesture in gesture_score_dict:
		label = gesture_score_dict[gesture][1]
		classes[label].append(gesture)

else:
	print('Classifying gestures using decision trees...')
	training_data = []
	for gesture in labeled_gestures:
		training_data.append(list(vector_data[gesture].values()))
	X = np.array(training_data)
	y = np.array(list(labeled_gestures.values()))
	tree = fit_decision_tree(X, y)

	for gesture in all_gestures:
		input_arr = list(vector_data[gesture].values())
		value = predict(tree, [input_arr]) # clf.predict returns a list, pick first element
		class_label = value[0]
		classes[class_label].append(gesture)
	
print('\nObtained the following classification:')
for k in classes:
	print('\nClass '+str(k))
	classes[k] = list(set(classes[k]))
	classes[k] = util.sortFileNames(classes[k])
	for g in classes[k]:
		print(g)
