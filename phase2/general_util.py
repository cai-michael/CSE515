import os
import platform

COMPONENTS = ['X','Y','Z','W']

WRD_FOLDER = 'wrd_data'
VECTOR_FOLDER = 'vector_data'
LATENT_SEMANTICS_FOLDER = 'latent_semantics_data'

# user_setting information
SAVE_DATA_FILE = 'user_settings.txt'
CSV_FOLDER = None
GAUSSIAN_BANDS = []
R = None
W = None
S = None

# OS-relative slash for file system navigation
SLASH = '\\' if ('Windows' in platform.system()) else '/'

# returns a list of the names of all files in 'directory' that end in 'extension'
def get_files(directory, extension):
	result = []
	for f in os.listdir(directory):
		if(len(f) >= len(extension)) and (f[len(f)-len(extension):len(f)] == extension):
			result.append(f)
	return result

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
	file.close()

# loads the data from SAVE_DATA_FILE
def load_user_settings():
	global CSV_FOLDER, R, W, S, GAUSSIAN_BANDS
	
	if (not os.path.exists(SAVE_DATA_FILE)):
		print('Error: could not find ' + SAVE_DATA_FILE)
		quit()
	
	lines = read_nonempty_lines(SAVE_DATA_FILE)
	for line in lines:
		if (': ' in line):
			ind = line.index(': ')
			variable = line[0:ind]
			value = line[ind + 2:len(line)]
			if (variable == 'CSV_FOLDER'):
				CSV_FOLDER = value
			elif (variable == 'R'):
				R = int(value)
				print('updated R to ' + str(R))
			elif (variable == 'W'):
				W = int(value)
			elif (variable == 'S'):
				S = int(value)
			elif (variable == 'GAUSSIAN_BANDS'):
				GAUSSIAN_BANDS = eval(value)



# reads a csv file and returns a list of lists of floats
def read_csv(file_path):
	result = read_nonempty_lines(file_path)
	result = list(map(lambda a : list(map(float, a.split(','))), result)) #split on commas and convert to floats
	return result



# most general function for reading a wrd file
# returns a dictionary {<component> : <component_data>} where:
# <component_data> is a dictionary {<sensor_id> : <sensor_data>} where:
# <sensor_data> is a dictionary {'avg':<avg>, 'std':<std>, 'series':<series_data>} where:
# <series_data> is a list of (<avgq>, <winq>) tuples
def read_wrd_general(file_path):
	lines = read_nonempty_lines(file_path)
	
	component = '?'
	sensor = -1
	result = {}
	for line in lines:
		if(line[0] == '#'): #command
			line = line[1:len(line)].split(' ')
			if(line[0] == 'component'):
				component = line[-1]
				result[component] = {}
			elif(line[0] == 'sensor'):
				sensor = int(line[-1])
				result[component][sensor] = {'avg':0.0, 'std':0.0, 'series':[]}
			elif(line[0] == 'avg') or (line[0] == 'std'):
				result[component][sensor][line[0]] = float(line[-1])
		else:
			line = line.split(' ')
			line = (float(line[0]), int(line[1]))
			result[component][sensor]['series'].append(line)
	return result

# reads a wrd file and returns a list of (component, sensor, winq) tuples
# the symbolic series
def read_wrd_symbolic(file_path):
	data = read_wrd_general(file_path)
	result = []
	for component in data:
		for sensor in data[component]:
			for tuple in data[component][sensor]['series']:
				result.append((component, sensor, tuple[1]))
	return result

# reads a wrd file and returns a list of (component, sensor, avgq) tuples
# the numerical series
def read_wrd_numerical(file_path):
	data = read_wrd_general(file_path)
	result = []
	for component in data:
		for sensor in data[component]:
			for tuple in data[component][sensor]['series']:
				result.append((component, sensor, tuple[0]))
	return result



# reads a txt storing a gesture vector and returns a dictionary {<word>:<value>}
# words are represented as '<component>;<sensor>;<winq>' strings
def read_vector_txt(file_path):
	lines = read_nonempty_lines(file_path)
	
	result = {}
	for line in lines:
		line = line.split(' ')
		result[line[0]] = float(line[1])
	return result


# Read vector txt as a list containing TF/TF-IDF values,
# in the order stored in the file
def read_vector_txt_to_list(file_path):
	lines = read_nonempty_lines(file_path)
	vector = [float(line.split(' ')[1]) for line in lines]
	return vector
