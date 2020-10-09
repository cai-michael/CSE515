from os import listdir
from collections import defaultdict
from copy import deepcopy
import re
import json
import math
import iohelpers

# Creates the gesture vector based on a directory d of word files
def createGestureVectors(d):
    # Determine all of the files that end with .wrd
    regex = re.compile(r'.*\.wrd')
    files = list(filter(regex.match, listdir(d)))
    data = []

    # For each data file process the input into one big dictionary
    for fileName in files:
        with open(d + "/" + fileName, 'r') as f:
            data += iohelpers.processInput(f)
    # Store the data as (gesture, sensor): time series data of words
    vectorData = iohelpers.compileData(data)

    # Calculate the TF, TFIDF, and TFIDF2 values for each (gesture, sensors)'s words
    tfValues = calculateTF(vectorData)
    tfidfValues = calculateTFIDF(vectorData, tfValues)
    tfidf2Values = calculateTFIDF2(vectorData, tfValues)
    wordIndexes = determineWordIndexes(vectorData)

    # Create vectors with a mapped word order based on the existence of the words
    totalWordCount = len(wordIndexes)
    lines = []
    wordOrder = [k for k, v in sorted(wordIndexes.items(), key=lambda item: item[1])]
    lines.append(str(wordOrder) + "\n")
    for gestureSensor, wordsList in tfValues.items():
        tfVector = [0] * totalWordCount
        tfidfVector = [0] * totalWordCount
        tfidf2Vector = [0] * totalWordCount
        for word in wordsList.keys():
            index = wordIndexes[word]
            tfVector[index] = tfValues[gestureSensor][word]
            tfidfVector[index] = tfidfValues[gestureSensor][word]
            tfidf2Vector[index] = tfidf2Values[gestureSensor][word]
        lines.append(str(gestureSensor) + "#" + str(tfVector) + "#" + str(tfidfVector) + "#" + str(tfidf2Vector) + "\n")

    # Write the data to the file vectors.txt
    with open(d + "/vectors.txt", "w+") as f:
        f.writelines(lines)

# Calculates the TF values n / K
def calculateTF(data):
    tfValues = {}
    # For each Gesture Sensor Pair
    for gestureSensor, values in data.items():
        tfValues[gestureSensor] = defaultdict(int)
        # Determine how many words are in the time-series
        totalWords = len(values)
        # Determine how many times a particualr word occurs within that time series
        for point in values:
            tfValues[gestureSensor][point] += 1
        # Find the proportion of a document (Gesture Sensor Pair) that is a particular word
        for k, v in tfValues[gestureSensor].items():
            tfValues[gestureSensor][k] = v / totalWords
    return tfValues

# Calculates the TFIDF utilizing TF * IDF considering each Gesture Sensor pair as an object
def calculateTFIDF(data, tfValues):
    idfValues = calculateIDFByGestureSensor(data)
    tfidf = deepcopy(tfValues)
    for k, v in tfValues.items():
        for index, tf in v.items():
            idf = idfValues[index]
            tfidf[k][index] = tf *  idf
    return tfidf

# Calculates the TFIDF utilizing TF * IDF considering each Gesture Sensor pair as an object
def calculateTFIDF2(data, tfValues):
    idfValues = calculateIDFByGesture(data)
    tfidf = deepcopy(tfValues)
    for k, v in tfValues.items():
        for index, tf in v.items():
            idf = idfValues[k[0]][index]
            tfidf[k][index] = tf *  idf
    return tfidf

# Calculate the IDF values log(N / m)
def calculateIDFByGestureSensor(data):
    sensorNum = 0
    pointFreq = defaultdict(int)
    # For each Gesture, Sensor Pair
    for values in data.values():
        sensorNum += 1
        # Determine how many Gesture Sensor pairs contain a particular word in their time-series
        for point in set(values):
            pointFreq[point] += 1
    # Find the log(How many Gesture Sensor pairs there are / The frequency of the word across all gesture sensor pairs)
    for k, v in pointFreq.items():
        pointFreq[k] = math.log(sensorNum / v)
    return pointFreq

# Calculates the IDF values only considering the sensors within one gesture
def calculateIDFByGesture(data):
    pointFreq = defaultdict(dict)
    idfValues = defaultdict(dict)
    sensorCount = defaultdict(int)
    # For each gesture sensor pair
    for gestureSensor, values in data.items():
        # Count how many sensors are in one gesture
        sensorCount[gestureSensor[0]] += 1
        if gestureSensor[0] not in pointFreq:
            pointFreq[gestureSensor[0]] = defaultdict(set)
        # Determine for one gesture how many sensors contain a particular words
        for point in set(values):
            pointFreq[gestureSensor[0]][point].add(gestureSensor[1])
    # Find the log(# Sensors in that Gesture / The frequency of the word across all sensors in that gesture)
    for gesture, secondDict in pointFreq.items():
        for point, sensors in secondDict.items():
            idfValues[gesture][point] = math.log(sensorCount[gesture] / len(sensors))
    return idfValues

# Creates a list of indexes for each word that was seen in the word files
def determineWordIndexes(data):
    allWords = defaultdict(tuple)
    wordIndex = 0
    for listOfWords in data.values():
        for word in listOfWords:
            if word not in allWords:
                allWords[word] = wordIndex
                wordIndex += 1
    return allWords

directory = str(input('Please enter the input directory: '))
createGestureVectors(directory)