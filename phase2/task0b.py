import os
from general_util import *
from task0_util import *

working_dir = os.getcwd()
wrd_dir = working_dir+SLASH+WRD_FOLDER
wrd_files = get_files(wrd_dir, '.wrd')

print('Found the following wrd files:')
for f in wrd_files:
	print(f)
print()



print('Reading wrd data...\n')
data = {}
for f in wrd_files:
	contents = read_wrd_general(working_dir+SLASH+WRD_FOLDER+SLASH+f)
	for component in contents:
		for sensor in contents[component]:
			contents[component][sensor] = list(map(lambda a : a[1], contents[component][sensor]['series']))
			#this reshapes the data so that it is a dictionary {<component>:<component_data>}
			#<component_data> is a dictionary {<sensor_id>:<series_data>}
			#<series_data> is a list of winq values
	data[f[0:-4]] = contents



#make sure the output directory exists
if(not VECTOR_FOLDER in os.listdir(working_dir)):
	os.mkdir(working_dir+SLASH+VECTOR_FOLDER)



print('Computing TF vectors...')
tf = {}
for f in data:
	tf[f] = {}
	for component in data[f]:
		for sensor in data[f][component]:
			#generate tf_vector for (component, sensor) pair of file f
			tf[f][component+', '+str(sensor)] = get_tf_vector(data[f][component][sensor])
	
	output_file = open(working_dir+SLASH+VECTOR_FOLDER+SLASH+'tf_vectors_'+f+'.txt','w')
	for key in tf[f]:
		output_file.write('#'+key+'\n')
		for winq in tf[f][key]:
			output_file.write(str(winq)+':'+str(tf[f][key][winq])+'\n')
		output_file.write('\n')
	output_file.close()
print('Finished.\n')



print('Computing TF-IDF vectors...')
print('NOT IMPLEMENTED')
quit()
print('Finished.\n')


