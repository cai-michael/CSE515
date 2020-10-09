from collections import defaultdict
from ast import literal_eval
import math
import re

# Returns a list containing tuples of the most similar gesture and the similarity score 
def determineMostSimilarGestures(directory, fileName, choice):
    f = re.sub(r'\.csv$', '', fileName)
    _, data = readVectors(directory, f, choice)
    querySensorData = data[f]
    distanceValues = defaultdict(float)
    for gesture, allSensors in data.items():
        if gesture != f:
            distanceValues[gesture] = compareGesture(querySensorData, allSensors)
    sortedValues = [(k, v) for k, v in sorted(distanceValues.items(), key=lambda item: item[1])]
    return sortedValues

# Calculate the distance between two gestures by using the square root of all squares of sensor distances
def compareGesture(querySensors, sensors):
    distances = []
    for s in sensors.keys():
        distances.append(compareSensor(querySensors[s], sensors[s]))
    distancesCount = len(distances)
    finalDistance = 0.0
    for i in range(distancesCount):
        finalDistance += distances[i] ** 2
    finalDistance = math.sqrt(finalDistance)
    return finalDistance

# Calculate the distance between two sensors as the normal distance function (square distance)
def compareSensor(queryVector, vector):
    totalSquares = 0.0
    wordCount = len(queryVector)
    for i in range(wordCount):
        totalSquares += (queryVector[i] - vector[i]) ** 2
    sensorDistance = math.sqrt(totalSquares)
    return sensorDistance

# Reads the vectors from vectors.txt file
def readVectors(directory, fileName, vectorToGet):
    data = defaultdict(dict)
    with open(directory + "/vectors.txt", "r") as f:
        lines = f.readlines()
        # Obtain the index keys for the words in the vectors
        keys = literal_eval(lines[0])
        for line in lines[1:]:
            raw = line.split('#')
            gestureSensor = literal_eval(raw[0])
            gesture = str(gestureSensor[0])
            sensor = gestureSensor[1]
            data[gesture][sensor] = literal_eval(raw[vectorToGet])
    return keys, data

# Removes delimiters and puts input into one data structure
def processInput(f):
    processedData = []
    for j in f:
        # Strip off newline characters/whitespace and then remove the initial set of brackets
        initialArray = j.strip()[2: -2].split("], [")
        for k, g in enumerate(initialArray):
            # Split the lists within the lists by commas and get rid of extra quotations or spaces
            initialArray[k] = list(map(lambda x: x.strip().replace('\'', ''), g.split(",")))
        processedData.append(initialArray)
    return processedData

directory = input('Please enter the name of directory of the gesture file to query: ')
gestureFile = input('Please enter the name of the gesture file to query on: ')
choice = int(input('Which value would you like to use in your query?\n1. TF\n2. TFIDF\n3. TFIDF2\n'))
similarGestures = determineMostSimilarGestures(directory, gestureFile, choice)

print('These are the most similar gestures to your choice:')
print('Rank\t|\tGesture\t|\tSimilarity Score\n')
for i in range(10):
    print(str(str(i + 1) + '\t|\t' + similarGestures[i][0]) + '\t|\t%.5f\n' % similarGestures[i][1]) 