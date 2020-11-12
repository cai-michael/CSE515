import os
import platform

COMPONENTS = ['X','Y','Z','W']

SAVE_DATA_FILE = 'user_settings.txt'
GRAPH_FOLDER = 'graph_data'

# OS-relative slash for file system navigation
SLASH = '\\' if ('Windows' in platform.system()) else '/'

#variables
CSV_FOLDER = None



# returns a list of the names of all files in 'directory' that end in 'extension'
def get_files(directory, extension):
	return list(filter(
		lambda f : (len(f) >= len(extension)) and (f[len(f)-len(extension):len(f)] == extension),
		os.listdir(directory)))

#check if a folder exists; if not, create it
def check_folder(directory, folder_name):
	if(folder_name in os.listdir(directory)):
		return True
	else:
		os.mkdir(directory + util.SLASH + folder_name)
		return False

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
	file.close()

# loads the data from SAVE_DATA_FILE
def load_user_settings():
	global CSV_FOLDER
	
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


