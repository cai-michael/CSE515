import math

#interpretation: max-min of the values for a (file,component,sensor)
#based on: Q&A from lecture 9/26/20
def get_average_amplitude(data):
	return max(data)-min(data)



#interpretation: square root of the average of the square distance from the mean for a (file,component,sensor)
def get_standard_deviation(data):
	mean = sum(data)/len(data)
	return math.sqrt(sum(map(lambda a : (a - mean)**2, data))/len(data))



#normalizes data into the -1.0 to 1.0 range
#converts all to 0.0 if data is all the same
def normalize(data):
	minval = min(data)
	maxval = max(data)
	if(maxval == minval):
		return list(map(lambda a : 0.0, data))
	return list(map(lambda a : 2.0*(a - minval)/(maxval - minval)-1.0, data))



#integral of normal distribution from a to b
def definite_gauss_integral(mu, sigma, a, b):
	#integral of Gaussian_mu_sigma from -Inf to a = math.erf((a-mu)/sigma/math.sqrt(2))/2
	a = math.erf((a-mu)/sigma/math.sqrt(2))/2
	b = math.erf((b-mu)/sigma/math.sqrt(2))/2
	return b-a

#computes a list of gaussian bands
#bands are represented by the divisions between them
def get_gaussian_bands(mu, sigma, r):
	coefficient = 2/definite_gauss_integral(mu, sigma, -1, 1)
	
	#compute the r unique band lengths
	band_lengths = []
	for i in range(r):
		i += 1
		band_lengths.append(coefficient*definite_gauss_integral(mu, sigma, (i-r-1)/r, (i-r)/r))
	
	#assemble the list of band lengths
	result = [0.0]
	temp = 0.0
	i = r-1
	while(i >= 0):
		temp -= band_lengths[i]
		result.insert(0,temp)
		result.append(-temp)
		i -= 1
	
	#correct endpoints
	result[0] = -1.0
	result[-1] = 1.0
	
	return result

#gives the index of the gaussian band to which x belongs
#indexes run from 0 to 2r-1
def get_band_index(bands, x):
	for i in range(len(bands)-1):
		if(x <= bands[i+1]):
			return i
	return len(bands)-2 #failsafe

#gives the midpoint of the gaussian band to which x belongs
def get_band_midpoint(bands, x):
	x = get_band_index(bands, x)
	return (bands[x]+bands[x+1])/2.0

#quantizes the values of data to the midpoints of the gaussian bands
def quantize(bands, data):
	return list(map(lambda a : get_band_midpoint(bands, a), data))



#returns a list of windows of length w separated by shift length s
def get_windows(data, w, s):
	result = []
	t = 0
	while(t+w <= len(data)):
		result.append(data[t:t+w])
		t += s
	return result



#creates a list of every possible word (every possible dimension in a gesture vector)
def get_possible_words(components, sensors, resolution):
	result = []
	for c in components:
		for s in sensors:
			for i in range(2*resolution):
				result.append(c+';'+str(s)+';'+str(i))
	return result

#takes a list of words and returns a dictionary of the form {<word>:<tf_value>}
#the tf_value for a given word is computed as: (number of instances of word in 'data') / (length of 'data')
#this is the k/N formula
#the word_list is used for determining the full range of possible words (i.e. the dimension of the tf vector)
def get_tf_vector(word_list, data):
	result = {}
	for word in word_list:
		result[word] = float(data.count(word)) / float(len(data))
	return result

#multiplies together the tf and idf vectors to create a tfidf vector
def get_tfidf_vector(tf_vector, idf_vector):
	result = {}
	for word in tf_vector:
		if (idf_vector[word] == None):
			result[word] = 0.0
		else:
			result[word] = tf_vector[word] * idf_vector[word]
	return result


