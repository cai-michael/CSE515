import math

#interpretation: average of the values for a (file,component,sensor)
def get_average_amplitude(data):
	return sum(data)/len(data)



#interpretation: average of the square distance from 'mean' for a (file,component,sensor)
def get_standard_deviation(data, mean):
	return sum(map(lambda a : (a - mean)**2, data))/len(data)



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



#returns a string of the form <n1,n2,...,nk> of band indexes of the window data
def get_symbolic_quantized_window_descriptor(bands, window):
	winq = list(map(lambda a : get_band_index(bands, a), window))
	winq = str(winq)
	winq = winq[1:-1] #remove brackets
	winq = winq.replace(' ','') #remove spaces
	winq = '<'+winq+'>'
	return winq


