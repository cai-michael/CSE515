# return the option that occurs most, or the earlier one if there's a tie
def majority_vote(votes):
	counts = {}
	for k in votes:
		if(not k in counts):
			counts[k] = 0
		counts[k] += 1
	cvalues = list(counts.values())
	return list(counts.keys())[cvalues.index(max(cvalues))]



# expresses the data_files as a compact string, abbreviating consecutive entries
def data_files_to_pretty_string(data_files):
	numeric = []
	nonnumeric = []
	
	for f in data_files:
		if(f.isnumeric()):
			numeric.append(int(f))
		else:
			nonnumeric.append(f)
	numeric.sort()
	
	# horrible list comprehension (but effective)
	numeric = [str(numeric[ind]) if (ind == 0) or (ind == len(numeric)-1) # preserve endpoints
		else (':' if (numeric[ind] == numeric[ind-1]+1) and (numeric[ind] == numeric[ind+1]-1)
			else str(numeric[ind]))
		for ind in range(len(numeric))]

	numeric = str(numeric)[1:-1].replace("'",'').replace(' ','')
	numeric = numeric.replace(':,',':').replace(',:',':')
	while('::' in numeric):
		numeric = numeric.replace('::',':')
	
	nonnumeric = str(nonnumeric)[1:-1].replace("'",'').replace(' ','')
	
	result = numeric+','+nonnumeric
	if(len(result) > 0) and (result[0] == ','):
		result = result[1:len(result)]
	if(len(result) > 0) and (result[-1] == ','):
		result = result[0:-1]
	return result.replace(',',', ')


