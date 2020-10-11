import os
import general_util as util
from task0_util import *

working_dir = os.getcwd()



#obtain the name of the gesture folder containing the X, Y, Z, W folders
print('Please specify the name of the gesture folder:')
util.CSV_FOLDER = input()
if(len(util.CSV_FOLDER) > 0):
	if(util.CSV_FOLDER[0] == util.SLASH):
		util.CSV_FOLDER = util.CSV_FOLDER[1:len(util.CSV_FOLDER)]
gesture_dir = working_dir + util.SLASH + util.CSV_FOLDER

print('Using directory '+gesture_dir)
print()

gesture_dir += util.SLASH



#ensure that all component directories are present
files = os.listdir(gesture_dir)
for c in util.COMPONENTS:
	if(not c in files):
		print('Error: missing component '+c)
		quit()

#create a non-redundant list of data files common to all component directories
data_files = set([])
for c in util.COMPONENTS:
	data_files = data_files.union(set(util.get_files(gesture_dir + c, '.csv')))
data_files = list(data_files)
data_files.sort()

print('Found the following data files:')
for f in data_files:
	print(f)
print()



#obtain RESOLUTION, WINDOW_LENGTH, and SHIFT_LENGTH
print('Please specify a desired resolution r:')
util.R = int(input())
print('Please specify a desired window length w:')
util.W = int(input())
print('Please specify a desired shift length s:')
util.S = int(input())
print()

util.save_user_settings()



#make sure the output directory exists
if(not util.WRD_FOLDER in os.listdir(working_dir)):
	os.mkdir(working_dir + util.SLASH + util.WRD_FOLDER)



#precompute the gaussian bands for later use
GAUSSIAN_BANDS = get_gaussian_bands(0, 0.25, util.R)



#main loop
print('Creating .wrd files...')
for f in data_files: #iterate over data files
	file_name = f[0:-4]
	output_file = open(working_dir + util.SLASH + util.WRD_FOLDER + util.SLASH + file_name+'.wrd','w')
	
	for c in util.COMPONENTS: #iterate over components
		output_file.write('#component '+c+'\n') #0a-1-a-i
		
		data = util.read_csv(gesture_dir + c + util.SLASH + f)
		
		for sensor in range(len(data)): #iterate over sensors
			output_file.write('#sensor '+str(sensor)+'\n') #0a-1-a-ii-A
			
			avg = get_average_amplitude(data[sensor])
			output_file.write('#avg '+str(avg)+'\n') #0a-1-a-ii-B
			
			std = get_standard_deviation(data[sensor])
			output_file.write('#std '+str(std)+'\n') #0a-1-a-ii-C
			
			data[sensor] = normalize(data[sensor]) #0a-1-a-ii-D
			
			data[sensor] = quantize(GAUSSIAN_BANDS, data[sensor]) #0a-1-a-ii-E
			
			data[sensor] = get_windows(data[sensor], util.W, util.S) #0a-1-a-ii-F
			
			for h in data[sensor]: #iterate over windows
				avgq = sum(h)/util.W #average amplitude of quantized data
				output_file.write(str(avgq)+' ') #0a-1-a-ii-G
				
				winq = get_band_index(GAUSSIAN_BANDS, avgq) #quantization of avgq
				winq = str(winq)
				output_file.write(str(winq)+'\n') #0a-1-a-ii-H
		output_file.write('\n')
	output_file.close()
print('Finished.')


