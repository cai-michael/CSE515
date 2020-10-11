import os
import platform

WRD_FOLDER = 'wrd_data'
COMPONENTS = ['X','Y','Z','W']
SLASH = '\\' if ('Windows' in platform.system()) else '/'



#returns a list of the names of all files in 'directory' that end in 'extension'
def get_files(directory, extension):
	result = []
	for f in os.listdir(directory):
		if(len(f) >= len(extension)) and (f[len(f)-len(extension):len(f)] == extension):
			result.append(f)
	return result

#extracts the nonempty lines from a file, formats them as a list
def read_nonempty_lines(file_path):
	result = []
	file = open(file_path, 'r')
	for q in file.readlines():
		q = q.replace('\n','').replace('\r','')
		if(len(q) > 0):
			result.append(q)
	file.close()
	return result



#reads a csv file and returns a list of lists of floats
def read_csv(file_path):
	result = read_nonempty_lines(file_path)
	result = list(map(lambda a : list(map(float, a.split(','))), result)) #split on commas and convert to floats
	return result



#most general function for reading a wrd file
#returns a dictionary {<component> : <component_data>} where:
#<component_data> is a dictionary {<sensor_id> : <sensor_data>} where:
#<sensor_data> is a dictionary {'avg':<avg>, 'std':<std>, 'series':<series_data>} where:
#<series_data> is a list of (<avgq>, <winq>) tuples
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

#reads a wrd file and returns a list of (component, sensor, winq) tuples
#the symbolic series
def read_wrd_symbolic(file_path):
	data = read_wrd_general(file_path)
	result = []
	for component in data:
		for sensor in data[component]:
			for tuple in data[component][sensor]['series']:
				result.append((component, sensor, tuple[1]))
	return result

#reads a wrd file and returns a list of (component, sensor, avgq) tuples
#the numerical series
def read_wrd_numerical(file_path):
	data = read_wrd_general(file_path)
	result = []
	for component in data:
		for sensor in data[component]:
			for tuple in data[component][sensor]['series']:
				result.append((component, sensor, tuple[0]))
	return result



#reads a txt file of gesture vectors and returns ???
def read_vectors_txt(file_path):
	print('read_vectors_txt NOT IMPLEMENTED')
	return []


