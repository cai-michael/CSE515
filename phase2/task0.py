import os
import platform
from general_util import *
from task0_util import *

OUTPUT_FOLDER = 'word_dictionaries'
COMPONENTS = ['X','Y','Z','W']

working_dir = os.getcwd()
SLASH = '\\' if ('Windows' in platform.system()) else '/'



#obtain the name of the gesture folder containing the X, Y, Z, W folders
print('Please specify the name of the gesture folder:')
gesture_dir = input()
if(len(gesture_dir) > 0):
	if(gesture_dir[0] != SLASH):
		gesture_dir = SLASH + gesture_dir
gesture_dir = working_dir + gesture_dir

print('Using directory \"'+gesture_dir+'\".\n')



#ensure that all component directories are present
files = os.listdir(gesture_dir)
for c in COMPONENTS:
	if(not c in files):
		print('Error: missing component '+c)
		quit()

#create a non-redundant list of data files common to all component directories
data_files = set([])
for c in COMPONENTS:
	data_files = data_files.union(set(get_files(gesture_dir+SLASH+c, '.csv')))
data_files = list(data_files)
data_files.sort()

print('Found the following data files:')
for f in data_files:
	print(f)
print()



#obtain RESOLUTION, WINDOW_LENGTH, and SHIFT_LENGTH
print('Please specify a desired resolution r:')
R = int(input())
print('Please specify a desired window length w:')
W = int(input())
print('Please specify a desired shift length s:')
S = int(input())
print()



#make sure the output directory exists
if(not OUTPUT_FOLDER in os.listdir(working_dir)):
	os.mkdir(working_dir+SLASH+OUTPUT_FOLDER)



#precompute the gaussian bands for later use
GAUSSIAN_BANDS = get_gaussian_bands(0, 0.25, R)



#main loop for 0a
print('Creating .wrd files...')
for f in data_files: #iterate over data files
	file_name = f[0:-4]
	output_file = open(working_dir+SLASH+OUTPUT_FOLDER+SLASH+file_name+'.wrd','w')
	
	for c in COMPONENTS: #iterate over components
		output_file.write('#component '+c+'\n') #0a-1-a-i
		
		data = read_csv(gesture_dir+SLASH+c+SLASH+f)
		
		for sensor in range(len(data)): #iterate over sensors
			output_file.write('#sensor '+str(sensor)+'\n') #0a-1-a-ii-A
			
			avg = get_average_amplitude(data[sensor])
			output_file.write('#avg '+str(avg)+'\n') #0a-1-a-ii-B
			
			std = get_standard_deviation(data[sensor], avg)
			output_file.write('#std '+str(std)+'\n') #0a-1-a-ii-C
			
			data[sensor] = normalize(data[sensor]) #0a-1-a-ii-D
			
			data[sensor] = quantize(GAUSSIAN_BANDS, data[sensor]) #0a-1-a-ii-E
			
			data[sensor] = get_windows(data[sensor], W, S) #0a-1-a-ii-F
			
			for h in data[sensor]: #iterate over windows
				avgq = get_average_amplitude(h) #average amplitude of quantized data
				output_file.write(str(avgq)+' ') #0a-1-a-ii-G
				
				winq = get_symbolic_quantized_window_descriptor(GAUSSIAN_BANDS, h)
				output_file.write(str(winq)+'\n') #0a-1-a-ii-H
		output_file.write('\n')
	output_file.close()
print('Finished.\n')



#main loop for 0b
print('Creating .txt vector files...')
print('NOT IMPLEMENTED')
quit()
print('Finished.\n')


