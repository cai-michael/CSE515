import os
#import copy
import math
import numpy as np
import general_util as util
from task0_util import *

working_dir = os.getcwd()

# Obtain the name of the gesture folder containing the X, Y, Z, W folders
util.CSV_FOLDER = input('Please specify the name of the gesture folder: ')
if (len(util.CSV_FOLDER) > 0):
	if (util.CSV_FOLDER[0] == util.SLASH):
		util.CSV_FOLDER = util.CSV_FOLDER[1:len(util.CSV_FOLDER)]
gesture_dir = working_dir + util.SLASH + util.CSV_FOLDER

print('Using directory ' + gesture_dir)
print()

gesture_dir += util.SLASH



# Ensure that all component directories are present
files = os.listdir(gesture_dir)
for c in util.COMPONENTS:
	if (not c in files):
		print('Error: missing component ' + c)
		quit()

# Create a non-redundant list of data files common to all component directories
data_files = set()
for c in util.COMPONENTS:
	data_files = data_files.union(set(util.get_files(gesture_dir + c, '.csv')))
for c in util.COMPONENTS:
	data_files = data_files.intersection(set(util.get_files(gesture_dir + c, '.csv')))
data_files = list(data_files)
data_files.sort()

print('Found the following data files:')
for f in data_files:
	print(f)
print()

# Strip '.txt' from file names
data_files = [f[0:-4] for f in data_files]



# Obtain RESOLUTION, WINDOW_SIZE, and SHIFT_LENGTH
util.R = int(input('Please specify a desired resolution r: '))
util.W = int(input('Please specify a desired window length w: '))
util.S = int(input('Please specify a desired shift length s: '))
print()



# Precompute the gaussian bands for later use
mu = 0
sigma = 0.25
util.GAUSSIAN_BANDS = get_gaussian_bands(mu, sigma, util.R)

util.save_user_settings()



# Preprocess the data (quantize, normalize)
print('Converting the data to .wrd')
util.check_folder(working_dir, util.WRD_FOLDER) # make sure the output directory exists

for f in data_files: # Iterate over data files
	output_file = open(working_dir + util.SLASH + util.WRD_FOLDER + util.SLASH + f +'.wrd','w')
	for c in util.COMPONENTS: # Iterate over components
		data = util.read_csv(gesture_dir + c + util.SLASH + f + '.csv')
		output_file.write('#component '+c+'\n')
		for sensor in range(len(data)): # Iterate over sensors
			data[sensor] = get_windows(data[sensor], util.W, util.S) #split into windows
			data[sensor] = [sum(a)/len(a) for a in data[sensor]] #convert each window to its average
			data[sensor] = normalize(data[sensor]) #normalize after splitting to get those sweet, sweet extreme values
			data[sensor] = symbolicize(data[sensor]) #quantize to band indices
			
			out = str(data[sensor])
			out = out.replace(' ','')[1:-1]
			#print(out)
			output_file.write(out+'\n')
	output_file.close()
print('Finished.\n')



print('Converting the data to gesture vectors...\n')
util.check_folder(working_dir, util.VECTOR_FOLDER)

data = {}
for f in data_files:
	data[f] = util.read_wrd_quantized(working_dir + util.SLASH + util.WRD_FOLDER + util.SLASH + f + '.wrd')
	data[f] = wrd_to_count_vector(data[f])

WORD_LIST = get_possible_words()

print('Computing TF vectors...')
tf = {}
for f in data:
	tf[f] = {}
	total = float(sum([data[f][word] for word in data[f]]))
	for word in data[f]:
		tf[f][word] = data[f][word]/total
	
	output_file = open(working_dir + util.SLASH + util.VECTOR_FOLDER + util.SLASH + 'tf_vector_' + f + '.txt','w')
	for word in tf[f]:
		output_file.write(word+' '+str(tf[f][word])+'\n')
	output_file.close()
print('Finished.\n')

print('Computing IDF values...')
idf = {}
for word in WORD_LIST:
	idf[word] = 0
	for f in data:
		idf[word] += 1 if (data[f][word] > 0) else 0 # Count files that contain the word -> m
	if(idf[word] == 0):
		idf[word] = None
	else:
		idf[word] = math.log(len(data) / idf[word]) # log(N/m)
print('Finished.\n')

print('Computing TF-IDF vectors...')
tfidf = {}
for f in data:
	tfidf[f] = {}
	for word in WORD_LIST:
		if (idf[word] == None):
			tfidf[f][word] = 0.0
		else:
			tfidf[f][word] = tf[f][word] * idf[word]
	
	output_file = open(working_dir + util.SLASH + util.VECTOR_FOLDER + util.SLASH + 'tfidf_vector_' + f + '.txt','w')
	for word in tfidf[f]:
		output_file.write(word+' '+str(tfidf[f][word])+'\n')
	output_file.close()
print('Finished.\n')



print('What metric would you like to use for the gesture-gesture similarity matrix?')
print('0: dot product')
print('1: negative Euclidean distance')
choice = int(input())

print('Computing gesture-gesture similarity matrix...')
util.check_folder(working_dir, util.GRAPH_FOLDER)

data_matrix = [list(tfidf[f].values()) for f in data]
data_matrix = np.matrix(data_matrix)
num_gestures, num_dimensions = np.shape(data_matrix)

similarity_matrix = []
if (choice == 0): # computes the similarity matrix using dot product
	similarity_matrix = np.matmul(data_matrix, data_matrix.transpose())
	similarity_matrix = similarity_matrix.tolist()
elif (choice == 1): # computes the similarity matrix using negative Euclidean distance
	for ind in range(num_gestures):
		one_vector = np.ones((num_gestures,1))
		gesture_vector = data_matrix[ind,:]
		distances = np.matmul(one_vector, gesture_vector)
		
		distances = np.subtract(distances, data_matrix)
		distances = np.multiply(distances, distances)
		
		one_vector = np.ones((num_dimensions,1))
		distances = np.matmul(distances, one_vector)
		distances = distances.transpose().tolist()[0]
		distances = [-math.sqrt(d) for d in distances]
		
		similarity_matrix.append(distances)

output_file = open(working_dir + util.SLASH + util.GRAPH_FOLDER + util.SLASH + 'similarity_matrix.txt','w')
output_file.write(str(list(data.keys())).replace(' ','').replace("'",'')[1:-1]+'\n')
for row in similarity_matrix:
	output_file.write(str(row).replace(' ','')[1:-1]+'\n')
output_file.close()

print('Finished.')


