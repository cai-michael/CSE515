import os
import general_util as util
from task0_util import *

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



# Make sure the output directory exists
util.check_folder(working_dir, util.WRD_FOLDER)



# Obtain RESOLUTION
print('Please specify a desired resolution r:')
util.R = int(input())



# Precompute the gaussian bands for later use
mu = 0
sigma = 0.25
util.GAUSSIAN_BANDS = get_gaussian_bands(mu, sigma, util.R)



# Preprocess the data (quantize, normalize)
print('Processing the .csv files')
for f in data_files: # Iterate over data files
	file_name = f[0:-4]
	#output_file = open(working_dir + util.SLASH + util.WRD_FOLDER + util.SLASH + file_name+'.wrd','w')
	
	for c in util.COMPONENTS: # Iterate over components
		data = util.read_csv(gesture_dir + c + util.SLASH + f)
		
		for sensor in range(len(data)): # Iterate over sensors
			data[sensor] = normalize(data[sensor])
			
			data[sensor] = quantize(data[sensor])
			
			data[sensor] = list(map(get_band_index, data[sensor]))
			
			print(str(data[sensor]).replace(' ',''))
	#output_file.close()



util.save_user_settings()