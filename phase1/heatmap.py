from collections import defaultdict
from ast import literal_eval
from os import listdir
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import iohelpers
import re

# Creates a heat map for one gesture where:
# Each sensor is rectangle where, within the rectangle each sesnor is one row and each column is one word
# VectorToGet takes 3 values
# 1 - TF
# 2 - TFIDF
# 3 - TFIDF2
def createHeatMap(d, gestureName, vectorToGet):

    name = re.sub(r'\.csv$', '', gestureName)

    # We want to grab the time series data to project the TF or TFIDF values
    with open(d + "/" + name + '.wrd', 'r') as f:
        rawTimeSeries = iohelpers.processInput(f)
    vectorData, timeValues = iohelpers.compileDataOneFile(rawTimeSeries)
    
    # Read the TF or TFIDF values for that particular gesture
    indexing, data = readVectors(d, name, vectorToGet)

    # Impose the TF or TFIDF values on the time series
    dataToImpose = createHeatMapRows(name, vectorData, indexing, data)

    # Create a dataframe to put the values in
    columnsToUse = list(timeValues)
    columnsToUse.sort()
    dataToMap = pd.DataFrame(columns=columnsToUse)

    for sensor, vector in dataToImpose.items():
        dataToMap.loc[sensor] = vector

    # Find the minimum and maximum values to scale the heatmap's colors
    maximumValue = dataToMap.to_numpy().max()
    minimumValue = dataToMap.to_numpy().min()

    # Set the size of the figure
    _, ax = plt.subplots(figsize=(15,15))

    # Plot the heatmap
    valueNames = ['TF', 'TF-IDF', 'TF-IDF2']
    sb.heatmap(dataToMap, cmap="Greys", vmin=minimumValue, vmax=maximumValue, linewidth=0.3, cbar_kws={"shrink": .8}, ax=ax)
    plt.xlabel("Time")
    plt.ylabel("Sensor")
    plt.title(valueNames[vectorToGet - 1] + " values for " + name)
    plt.show()
    return
    
# Reads the vectors from vectors.txt file
def readVectors(directory, fileName, vectorToGet):
    data = defaultdict(list)
    with open(directory + "/vectors.txt", "r") as f:
        lines = f.readlines()
        # Obtain the index keys for the words in the vectors
        keys = literal_eval(lines[0])
        for line in lines[1:]:
            raw = line.split('#')
            gestureSensor = literal_eval(raw[0])
            # We only care about the vectors for a certain file
            if str(gestureSensor[0]) == fileName:
                data[gestureSensor[1]] = literal_eval(raw[vectorToGet])
    return keys, data

# Creates the rows based on the time series by replacing the words with the TF or TFIDF values
def createHeatMapRows(name, timeSeries, indexing, values):
    finalRows = defaultdict(list)
    intermediateRows = defaultdict(list)
    for gestureSensor, series in timeSeries.items():
        if str(gestureSensor[0]) == name:
            intermediateRows[gestureSensor[1]] = series
    for sensor, row in intermediateRows.items():
        finalRows[sensor] = []
        for word in row:
            vectorIndex = indexing.index(word)
            vectorReference = values[sensor]
            finalRows[sensor].append(vectorReference[vectorIndex])

    return finalRows

directory = input('Please enter the name of directory of the gesture file to view: ')
gestureFile = input('Please enter the name of the gesture file to view: ')
choice = int(input('Which heatmap would you like to see?\n1. TF\n2. TFIDF\n3. TFIDF2\n'))
createHeatMap(directory, gestureFile, choice)