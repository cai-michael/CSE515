import os



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



#reads a wrd file and returns a list of (component, sensor, winq) tuples
def read_wrd(file_path):
	lines = read_nonempty_lines(file_path)
	
	component = '?'
	sensor = -1
	result = []
	for line in lines:
		if(line[0] == '#'): #command
			line = line[1:len(line)].split(' ')
			if(line[0] == 'component'):
				component = line[-1]
			elif(line[0] == 'sensor'):
				sensor = int(line[-1])
		else:
			line = line.split(' ')
			line = line[-1] #take only the winq
			result.append((component, sensor, line))
	
	return result



#reads a txt file of gesture vectors and returns ???
def read_vectors_txt(file_path):
	print('read_vectors_txt NOT IMPLEMENTED')
	return []


