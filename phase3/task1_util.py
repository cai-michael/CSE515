def createPlot(dataToGraph, ax):
    for sensorID, sensorData in enumerate(dataToGraph):
        time = list(range(0, len(sensorData)))
        # plotting the line 1 points 
        ax.plot(time, sensorData, label = f"Sensor {sensorID}")