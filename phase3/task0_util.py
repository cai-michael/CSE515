import math
import general_util as util



#normalizes data into the -1.0 to 1.0 range
#converts all to 0.0 if data is all the same
def normalize(data):
	minval = min(data)
	maxval = max(data)
	if(maxval == minval):
		return [0.0 for x in data]
	return [2.0*(x - minval)/(maxval - minval)-1.0 for x in data]



# integral of normal distribution from a to b
def definite_gauss_integral(mu, sigma, a, b):
	#integral of Gaussian_mu_sigma from -Inf to a = math.erf((a-mu)/sigma/math.sqrt(2))/2
	a = math.erf((a-mu)/sigma/math.sqrt(2))/2
	b = math.erf((b-mu)/sigma/math.sqrt(2))/2
	return b-a

# computes a list of gaussian bands
# bands are represented by the divisions between them
def get_gaussian_bands(mu, sigma, r):
	coefficient = 2/definite_gauss_integral(mu, sigma, -1, 1)
	
	# compute the r unique band lengths
	band_lengths = []
	for i in range(r):
		i += 1
		band_lengths.append(coefficient*definite_gauss_integral(mu, sigma, (i-r-1)/r, (i-r)/r))
	
	# assemble the list of band lengths
	result = [0.0]
	temp = 0.0
	i = r-1
	while (i >= 0):
		temp -= band_lengths[i]
		result.insert(0,temp)
		result.append(-temp)
		i -= 1
	
	# correct endpoints
	result[0] = -1.0
	result[-1] = 1.0
	
	return result

# gives the index of the gaussian band to which x belongs
# indexes run from 0 to 2r-1
def get_band_index(x):
	for i in range(len(util.GAUSSIAN_BANDS)-1):
		if(x <= util.GAUSSIAN_BANDS[i+1]):
			return i
	return len(util.GAUSSIAN_BANDS)-2 #failsafe

# gives the midpoint of the gaussian band to which x belongs
def get_band_midpoint(x):
	x = get_band_index(x)
	return (util.GAUSSIAN_BANDS[x]+util.GAUSSIAN_BANDS[x+1])/2.0

# quantizes the values of data to the midpoints of the gaussian bands
def quantize(data):
	return [get_band_midpoint(x) for x in data]



