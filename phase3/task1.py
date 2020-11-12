import os
import general_util as util

working_dir = os.getcwd()

# Obtain the name of the gesture folder containing the X, Y, Z, W folders
print('Please specify the name of the gesture folder:')
util.CSV_FOLDER = input()
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



# Make sure the output directories exist
util.check_folder(working_dir, util.GRAPH_FOLDER)



#create similarity graph



util.save_user_settings()