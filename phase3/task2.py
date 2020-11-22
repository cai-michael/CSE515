import os
import general_util as util
import task0_util as task0
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
# print(labeled_gestures)
# print(classes)

all_gestures = set(data_files)
# Identify the unclassified gestures
unclassified_gestures = set(data_files)
unclassified_gestures = unclassified_gestures.difference(set(labeled_gestures.keys()))
unclassified_gestures = list(unclassified_gestures)


# Each classification method should add unclassified_gestures to the lists in the 'classes' dictionary
if(classifier == 1):
    distance_metric = lambda a, b : task0.euclidean_distance(vector_data[a], vector_data[b])
    hit = 0;
    total = 0;
    print('Please select the degree k for nearest neighbors:')
    k = int(input())

    print('Classifying gestures using '+str(k)+' nearest neighbors...')
    for g in labeled_gestures: # unclassified_gestures:
        distances = {f : distance_metric(g, f) for f in labeled_gestures} # compute dict of distances
        ranking = sorted(distances.keys(), key=lambda f : distances[f])
        ranking = ranking[0:k]
        ranking = [labeled_gestures[f] for f in ranking] # get labels
        final_vote = majority_vote(ranking)
        int_gesture = int(g)
        actual_label = None
        if int_gesture <= 31:
            actual_label = 0
        elif int_gesture < 559:
            actual_label = 1
        else:
            actual_label = 2
        if actual_label == final_vote:
            hit +=1
        total += 1
        classes[majority_vote(ranking)].append(g)
    print("final score")
    print(hit/total)

elif(classifier == 2):
    print('Classifying gestures using personalized page rank...')
    similarity_graph = util.read_similarity_graph(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt')
    transition_matrix = create_transition_matrix(similarity_graph)

    # a dictionary to track the highest PPR score and class label for a gesture
    gesture_score_dict = {}
    gesture_index_in_graph = list(similarity_graph.keys())
    for label in classes:
        labeled_gestures_in_class = classes[label]
        print(labeled_gestures_in_class)

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

    print(gesture_score_dict)
    for gesture in gesture_score_dict:
        label = gesture_score_dict[gesture][1]
        classes[label].append(gesture)

else:
    print('Classifying gestures using decision trees...')
    training_data = []
    for gesture in labeled_gestures:
        training_data.append(list(vector_data[gesture].values()))
    X = np.array(training_data)
    print(X.shape)
    y = np.array(list(labeled_gestures.values()))  # pylint: disable=no-member
    print(y)
    clf = DecisionTreeClassifier(max_depth=1000)
    clf.fit(X, y)

    clf_dict = {}
    hit = 0
    total = 0
    for gesture in all_gestures:
        int_gesture = int(gesture)
        actual_label = None
        if int_gesture <= 31:
            actual_label = 0
        elif int_gesture < 559:
            actual_label = 1
        else:
            actual_label = 2
        input_arr = list(vector_data[gesture].values())
        value = clf.predict([input_arr])
        clf_dict[gesture] = value[0]
        if actual_label == value[0]:
            hit += 1
        total += 1
    print(clf_dict)
    print(hit/total)

#print(labeled_gestures)
print('\nObtained the following classification:')
for k in classes:
	print('\nClass '+str(k))
	sorted_classes = set(classes[k].sort(key=lambda a: int(a))) # WARNING: will break for non-numeric gesture names
	for g in sorted_classes[k]:
		print(g)
