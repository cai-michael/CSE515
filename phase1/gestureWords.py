from os import listdir
import numpy as np
import pandas as pd
import math
import re

# Constants
mean = 0
std = 0.25

"""
Creates a gesture words dictionary using:
d:  Directory Name
w:  Window Length
s:  Shift Length
r:  Resolution
"""
def createGestureWords(d, w, s, r):
    regex = re.compile(r'.*\.csv')
    files = list(filter(regex.match, listdir(d)))

    # For each data file
    for f in files:
        path = d + "/" + f
        rawData = pd.read_csv(path, header=None)

        # Normalize the full file
        normData = rawData.apply(lambda x: (2 * (x - x.min()) / (x.max() - x.min())) - 1, axis=1)

        # Quantize the entries into 2 * r levels
        quantizedData = quantize(normData, r)

        f = re.sub(r'\.csv$', '', f)

        # Create word dictionary
        words = createWords(quantizedData, w, s, f)
        
        # Save the data as f.wrd
        with open(d + '/' + f + '.wrd', 'w') as outputFile:
            outputFile.writelines("%s\n" % word for word in words)

# Creates words based on the data, window frame, shift length, and file name
def createWords(data, w, s, f):
    finalData = []
    numRows = len(data.index)
    for i in range(numRows):
        j = 0
        while j + w <= len(data.columns):
            element = []
            # Grab a window of w
            for k in range(w):
                element.append(data[j + k][i])
            # Add element to greater list
            finalData.append([ [ f, i, j ], element ])
            # Shift s
            j += s

    return finalData       

# Quantizes the data into bands
def quantize(data, r):
    bands = get_bands(r)
    return data.applymap(lambda x: determine_band(x, bands, r))

# Integrates from lower to upper bound
def gaussian_distribution_integral(mean, std, lower, upper):
    low = math.erf((lower - mean) / std / math.sqrt(2)) / 2
    high = math.erf((upper - mean) / std / math.sqrt(2)) / 2
    return high - low
    
# Determines the band of value (bands go from 1 to 2r (-1 to 1))
def determine_band(value, bands, r):
    for i in range(2 * r - 1):
        if value <= bands[i]:
            return i + 1
    return 2 * r

# Determine the cutoffs for the bands
def get_bands(r):
    # Compute Lengths
    lengths = []
    denominator = gaussian_distribution_integral(mean, std, -1, 1)
    for i in range(1, 2 * r + 1):
        numerator = gaussian_distribution_integral(mean, std, (i - r - 1) / r, (i - r) / r)
        lengths.append(2 * numerator / denominator)

    #Compute band cutoffs
    bands = []
    currentBoundary = 0.0
    i = r - 1
    while(i > 0):
        currentBoundary -= lengths[i]
        bands.append(currentBoundary)
        i -= 1

    # Reverse the negative values and add the center cutoff of 0
    bands.reverse()
    bands.append(0.0)

    currentBoundary = 0.0
    i = r
    while(i < len(lengths) - 1):
        currentBoundary += lengths[i]
        bands.append(currentBoundary)
        i += 1

    return bands

directory = str(input('Please enter the input directory: '))
window = int(input('Please enter a window frame for creating words: '))
shift = int(input('Please enter a shift value for creating words: '))
resolution = int(input('Please enter a resolution for calculating word bands: '))
createGestureWords(directory, window, shift, resolution)