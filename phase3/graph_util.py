import numpy as np

def create_similarity_graph(degree, similarity_matrix, vertices=None):
	graph = {}
	for row in range(len(similarity_matrix)):
		temp = similarity_matrix[row].tolist()[0]
		temp = sorted(range(len(temp)), reverse=True, key=lambda a: temp[a])
		
		if(row in temp):
			del temp[temp.index(row)]
		temp = temp[0:degree]
		
		graph[row] = temp
	
	if(vertices != None): #rename vertices
		for row in range(len(similarity_matrix)):
			graph[row] = [vertices[a] for a in graph[row]]
			graph[vertices[row]] = graph[row]
			del graph[row]
	
	return graph

#creates a transition matrix M where M[i,j] indicates where there is an edge from j to i
def create_transition_matrix(graph):
	vertices = list(graph.keys())
	matrix = np.zeros((len(vertices), len(vertices)))
	for column in range(len(vertices)):
		num_transitions = len(graph[vertices[column]])
		if(num_transitions > 0):
			for row in range(len(vertices)):
				if(vertices[row] in graph[vertices[column]]):
					matrix[row, column] = 1.0/num_transitions
	return matrix



def personalized_page_rank(transition_matrix, init_vector, restart_probability, max_iterations=1000):
	walk_vector = init_vector.copy()
	for i in range(max_iterations):
		new_vector = np.add((1.0 - restart_probability) * np.matmul(transition_matrix, walk_vector), restart_probability * init_vector)
		if(np.linalg.norm(np.subtract(new_vector, walk_vector)) == 0.0): #check for no change
			return new_vector
		walk_vector = new_vector
	return walk_vector


