import os
import math
import general_util as util
from task0_util import *

SENSORS = []
util.load_user_settings()

working_dir = os.getcwd()
wrd_dir = working_dir + util.SLASH + util.WRD_FOLDER
wrd_files = util.get_files(wrd_dir, '.wrd')

print('Found the following wrd files:')
for f in wrd_files:
	print(f)
print()



print('Reading wrd data...\n')
data = {}
for f in wrd_files:
	file_name = f[0:-4]
	data[file_name] = util.read_wrd_symbolic(working_dir+util.SLASH+util.WRD_FOLDER+util.SLASH+f) # Read tuple list
	
	if (len(SENSORS) == 0):
		for q in data[file_name]:
			if(not q[1] in SENSORS):
				SENSORS.append(q[1])
	
	# Convert tuples to strings
	data[file_name] = list(map(lambda a : a[0]+';'+str(a[1])+';'+str(a[2]), data[file_name]))



# Make sure the output directory exists
if (not util.VECTOR_FOLDER in os.listdir(working_dir)):
	os.mkdir(working_dir+util.SLASH+util.VECTOR_FOLDER)



# Find all possible words
WORD_LIST = get_possible_words(util.COMPONENTS, SENSORS, util.R)



print('Computing TF vectors...')
tf = {}
for f in data:
	tf[f] = get_tf_vector(WORD_LIST, data[f])
	
	#write to output_file
	output_file = open(working_dir+util.SLASH+util.VECTOR_FOLDER+util.SLASH+'tf_vectors_'+f+'.txt','w')
	for word in tf[f]:
		output_file.write(word+' '+str(tf[f][word])+'\n')
	output_file.close()
print('Finished.\n')



print('Computing IDF values...')
idf = {}
for word in WORD_LIST:
	idf[word] = 0
	for f in data:
		if(word in data[f]):
			idf[word] += 1 # Count files that contain the word -> m
	if(idf[word] == 0):
		idf[word] = None
	else:
		idf[word] = math.log(len(data) / idf[word]) # log(N/m)
print('Finished.\n')



print('Computing TF-IDF vectors...')
tfidf = {}
for f in data:
	tfidf[f] = get_tfidf_vector(tf[f], idf)
	
	#write to output_file
	output_file = open(working_dir+util.SLASH+util.VECTOR_FOLDER+util.SLASH+'tfidf_vectors_'+f+'.txt','w')
	for word in tfidf[f]:
		output_file.write(word+' '+str(tfidf[f][word])+'\n')
	output_file.close()
print('Finished.')


