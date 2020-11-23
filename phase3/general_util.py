import os
import platform
import shutil
import numpy as np

COMPONENTS = ['X','Y','Z','W']
SENSOR_COUNT = 20

SAVE_DATA_FILE = 'user_settings.txt'
WRD_FOLDER = 'wrd_data'
VECTOR_FOLDER = 'vector_data'
GRAPH_FOLDER = 'graph_data'
PLOT_FOLDER = 'gesture_plots'

# OS-relative slash for file system navigation
SLASH = '\\' if ('Windows' in platform.system()) else '/'

# variables
CSV_FOLDER = None
R = None # resolution
W = None # window size
S = None # shift length
DEGREE = None # similarity graph degree
GAUSSIAN_BANDS = []



# returns a list of the names of all files in 'directory' that end in 'extension'
def get_files(directory, extension):
	return list(filter(
		lambda f : (len(f) >= len(extension)) and (f[len(f)-len(extension):len(f)] == extension),
		os.listdir(directory)))

# check if a folder exists; if not, create it
def check_folder(directory, folder_name, deleteFirst=False):
	if(folder_name in os.listdir(directory)):
		if deleteFirst:
			shutil.rmtree(directory + SLASH + folder_name)
			os.mkdir(directory + SLASH + folder_name)
		return True
	else:
		os.mkdir(directory + SLASH + folder_name)
		return False

def remove_files_in_folder(directory, fileNames):
	for f in fileNames:
		os.remove(directory + f)
	return

# extracts the nonempty lines from a file, formats them as a list
def read_nonempty_lines(file_path):
	result = []
	file = open(file_path, 'r')
	for q in file.readlines():
		q = q.replace('\n','').replace('\r','')
		if(len(q) > 0):
			result.append(q)
	file.close()
	return result



# saves user choices for later reference
def save_user_settings():
	file = open(SAVE_DATA_FILE, 'w')
	file.write('CSV_FOLDER: ' + CSV_FOLDER + '\n')
	file.write('R: '+ str(R) + '\n')
	file.write('W: '+ str(W) + '\n')
	file.write('S: '+ str(S) + '\n')
	file.write('GAUSSIAN_BANDS: ' + str(GAUSSIAN_BANDS) + '\n')
	file.write('DEGREE: '+ str(DEGREE) + '\n')
	file.close()

# loads the data from SAVE_DATA_FILE
def load_user_settings():
	global CSV_FOLDER, R, W, S, DEGREE
	
	if (not os.path.exists(SAVE_DATA_FILE)):
		print('Error: could not find ' + SAVE_DATA_FILE)
		quit()
	
	lines = read_nonempty_lines(SAVE_DATA_FILE)
	for line in lines:
		if (': ' in line):
			ind = line.index(': ')
			variable = line[0:ind]
			value = line[ind + 2:len(line)]
			if(value != 'None'):
				if (variable == 'CSV_FOLDER'):
					CSV_FOLDER = value
				elif (variable == 'R'):
					R = int(value)
				elif (variable == 'W'):
					W = int(value)
				elif (variable == 'S'):
					S = int(value)
				elif (variable == 'GAUSSIAN_BANDS'):
					GAUSSIAN_BANDS = eval(value)
				elif (variable == 'DEGREE'):
					DEGREE = int(value)



# reads a csv file and returns a list of lists of floats
def read_csv(file_path):
	result = read_nonempty_lines(file_path)
	result = [[float(val) for val in line.split(',')] for line in result] # split on commas and convert to floats
	return result

# reads a wrd file and returns a dictionary {component: [sensor1 = [1, 3, 0, 1...], sensor2 = [...]...]}
def read_wrd_quantized(file_path):
	result = {}
	component = None
	for line in read_nonempty_lines(file_path):
		if(line[0] == '#'):
			line = line[1:len(line)].split(' ')
			if(line[0] == 'component'):
				component = line[-1]
				result[component] = []
		else:
			line = line.split(',')
			line = [int(x) for x in line]
			result[component].append(line)
	return result

# same as read_wrd_quantized, but gives the band midpoints instead
def read_wrd(file_path):
	result = read_wrd_quantized(file_path)
	for c in result:
		for sensor_id in range(len(result[c])):
			result[c][sensor_id] = [(GAUSSIAN_BANDS[x] + GAUSSIAN_BANDS[x+1])/2.0 for x in result[c][sensor_id]]
	return result



# returns {'component;sensor;word' : float}
def read_vector(file_path):
	result = {}
	for line in read_nonempty_lines(file_path):
		line = line.split(' ')
		line[1] = float(line[1])
		result[line[0]] = line[1]
	return result



# returns (file_names, similarity_matrix)
def read_similarity_matrix(file_path):
	matrix = read_nonempty_lines(file_path)
	files = matrix[0].split(',')
	matrix = matrix[1:len(matrix)]
	matrix = [list(map(float, line.split(','))) for line in matrix]
	matrix = np.matrix(matrix)
	return (files, matrix)

def read_similarity_graph(file_path):
	graph = {}
	for line in read_nonempty_lines(file_path):
		line = line.split(': ')
		graph[line[0]] = line[1].split(',')
	return graph


def tuplifyNames(names):
	# Find the name with the most underscores
	tupleLength = 1
	for name in names:
		newLength = name.count('_') + 1
		if tupleLength < newLength:
			tupleLength = newLength

	# Create tuples based on the names
	tuples = []
	for name in names:
		words = name.split('_')
		tupleToAppend = [-1] * tupleLength
		for idx, value in enumerate(words):
			tupleToAppend[idx] = int(value)
		tuples.append(tuple(tupleToAppend))
	tuples.sort()
	return tuples

def removeAllOccurrences(listToCheck, value):
	while value in listToCheck:
		listToCheck.remove(value)
	return listToCheck

def sortFileNames(names):
	tuplifiedNames = tuplifyNames(names)
	stringifiedNames = [list(str(x) for x in tup) for tup in tuplifiedNames]
	adjustedNames = [removeAllOccurrences(tup, '-1') for tup in stringifiedNames]
	sortedNames = ['_'.join(tups) for tups in adjustedNames] 
	return sortedNames
