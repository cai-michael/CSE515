# Compiles the data into one dictionary for gesture sensor pairs
def compileData(data):
    newData = {}
    for x in data:
        # Obtain the gesture and sensor as a tuple for identification
        gestureSensor = tuple((x[0][0], int(x[0][1])))
        # Add a new dictionary if the sensor increments
        if not gestureSensor in newData:
            newData[gestureSensor] = []
        # Convert the key array into ints
        newData[gestureSensor].append(tuple(map(lambda x: int(x), x[1])))
    return newData

# Compiles the data into one dictionary for gesture sensor pairs
def compileDataOneFile(data):
    timeValues = set()
    newData = {}
    for x in data:
        # Obtain the gesture and sensor as a tuple for identification
        gestureSensor = tuple((x[0][0], int(x[0][1])))
        timeValues.add(int(x[0][2]))
        # Add a new dictionary if the sensor increments
        if not gestureSensor in newData:
            newData[gestureSensor] = []
        # Convert the key array into ints
        newData[gestureSensor].append(tuple(map(lambda x: int(x), x[1])))
    return newData, timeValues

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

