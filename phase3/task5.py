import general_util as util
from graph_util import *
import os

task3_dir = "lsh_outputs"
working_dir = os.getcwd()
top_t_gestures = []
# Retrieve top t gestures form task3
with open(task3_dir + "/task3_results") as f:
    for line in f:
        if "|" not in line:
            task3_results = line.split()
            top_t_gestures.append(task3_results[1])
    print("Top t gestures results from task3:")
for i in range(len(top_t_gestures)):
    print(top_t_gestures[i])
print("\n")

# Assign gestures to be relevant or irrelevant
print('Which gestures would you like to list as relevant? (e.g. 1, 249, 559, etc.):')
relevant_gestures = input().replace(' ', '').split(',')
print('Which gestures would you like to list as irrelevant? (e.g. 2, 258, 537, etc.):')
irrelevant_gestures = input().replace(' ', '').split(',')

#PPR
# Retrieve similiarity matrix, graph, and data files to use in calculation
data_files, similarity_matrix = util.read_similarity_matrix(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt')

similarity_graph = util.read_similarity_graph(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_graph.txt')

# remove irrelevant gestures from similarity_graph
for gesture in irrelevant_gestures:
    for g in similarity_graph:
        if gesture in similarity_graph[g]:
            similarity_graph[g].pop(similarity_graph[g].index(gesture))

# Build transition matrix
transition_matrix = create_transition_matrix(similarity_graph)

# initialize seed gestures with the relevant gestures
seed_gestures = list(filter(lambda a : a in data_files, relevant_gestures))
seed_gestures = list(set(seed_gestures)) # remove redundancies

# Compute dominant gestures
init_vector = np.zeros((len(data_files), 1))
for gesture in seed_gestures:
    init_vector[data_files.index(gesture), 0] = 1.0/len(seed_gestures)

ppr = personalized_page_rank(transition_matrix, init_vector, 0.1)
gesture_score_dict = {}
gesture_index_in_graph = list(similarity_graph.keys())

dominant_gestures = ppr.transpose().tolist()[0]
dominant_gestures = sorted(range(len(dominant_gestures)), reverse=True, key=lambda a : dominant_gestures[a])
dominant_gestures = [data_files[a] for a in dominant_gestures]

#print(dominant_gestures[10])
#print(gesture_score_dict)
print(f'Classifier-based relevance feedback:')
for gesture in dominant_gestures:
    if gesture in top_t_gestures:
        print(gesture)
# get task 3 output, user will mark which ones are relevant and irreleveant
# revelant <- uses for the vector nodes in PPR
# irrelevant <- remove them from the similarity matrix
# print out the new strongest components