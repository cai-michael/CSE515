import general_util as util
import os
import numpy as np

working_dir = os.getcwd()

# Make sure the output directory exists
util.check_folder(working_dir, util.GRAPH_FOLDER)

data_files, similarity_matrix = util.read_similarity_matrix(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt')

print(len(data_files))
print(data_files)
print(np.shape(similarity_matrix))
print(similarity_matrix)



# Create similarity graph
print('Creating a gesture similarity graph...')



# Request seed gestures



# Compute dominant gestures



# Visualize dominant gestures


