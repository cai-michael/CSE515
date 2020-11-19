import general_util as util
import task0_util as task0
from task2_util import *
from graph_util import *

print('Which classifier would you like to use?')
print('1: k nearest neighbors')
print('2: personalized page rank')
print('3: decision trees')

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



# TO DO: populate this from user input somehow
labeled_gestures = {} # dict of form {gesture name : label}
labeled_gestures['1'] = 0
labeled_gestures['3'] = 0
labeled_gestures['21'] = 0
labeled_gestures['260'] = 1
labeled_gestures['267'] = 1
labeled_gestures['273'] = 1
labeled_gestures['577'] = 2
labeled_gestures['587'] = 2
labeled_gestures['589'] = 2

classes = {} # dict of form {label : [gesture names]}
for g in labeled_gestures:
	if(not labeled_gestures[g] in classes):
		classes[labeled_gestures[g]] = []
	classes[labeled_gestures[g]].append(g)



# Identify the unclassified gestures
unclassified_gestures = set(data_files)
unclassified_gestures = unclassified_gestures.difference(set(labeled_gestures.keys()))
unclassified_gestures = list(unclassified_gestures)



# Each classification method should add unclassified_gestures to the lists in the 'classes' dictionary
if(classifier == 1):
	#distance_metric = task0.euclidean_distance
	distance_metric = lambda a, b : task0.euclidean_distance(vector_data[a], vector_data[b])
	
	print('Please select the degree k for nearest neighbors:')
	k = int(input())
	
	print('Classifying gestures using '+str(k)+' nearest neighbors...')
	for g in unclassified_gestures:
		distances = {f : distance_metric(g, f) for f in labeled_gestures} # compute dict of distances
		ranking = sorted(distances.keys(), reverse=False, key=lambda f : distances[f])
		ranking = ranking[0:k]
		ranking = [labeled_gestures[f] for f in ranking] # get labels
		classes[majority_vote(ranking)].append(g)
	
elif(classifier == 2):
	print('Classifying gestures using personalized page rank...')
	# probably need to load in the similarity graph from task 1 here
else:
	print('Classifying gestures using decision trees...')
	# TO DO



print('\nObtained the following classification:')
for k in classes:
	print('\nClass '+str(k))
	classes[k].sort(key=lambda a: int(a)) # WARNING: will break for non-numeric gesture names
	for g in classes[k]:
		print(g)
