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



print('\nPlease specify the number of distinct labels for classification:')
labeled_gestures = {} # dict of form {gesture name : label}
classes = {label : [] for label in range(int(input()))} # dict of form {label : [gesture names]}
print('\nTo specify the gestures in a label, use a comma-separated list. (e.g. "1, 3, 8")')
print('You can also specify ranges using a colon. (e.g. "5:9")')
print('Select files from: '+data_files_to_pretty_string(data_files)+'\n')

for label in classes:
	print('Please specify just the gestures for label '+str(label)+'.')
	command = input().replace(' ','').split(',')
	for word in command:
		if(':' in word): # specify a range
			word = word.split(':')
			if(word[0].isnumeric() and word[1].isnumeric()):
				word[0] = int(word[0])
				word[1] = int(word[1])
				word[0], word[1] = min(word[0], word[1]), max(word[0], word[1])
				word = set([str(a) for a in range(word[0], word[1]+1)])
				word = list(word.intersection(set(data_files)))
				for w in word:
					labeled_gestures[w] = label
					classes[label].append(w)
		elif(word in data_files):
			labeled_gestures[word] = label
			classes[label].append(word)
#print(labeled_gestures)
#print(classes)
print()



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
