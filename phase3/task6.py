import math
import os
import numpy as np
import general_util as util
from task2_util import *
from graph_util import *

working_dir = os.getcwd()

# list of the names of all gestures in the database
data_files = util.get_files(util.WRD_FOLDER,'.wrd')
data_files = [a[0:-4] for a in data_files] # strip file extension

# Get user input 
print('Please select the gesture to use a query object')
queryGesture = input()

while queryGesture not in data_files:
    print('Invalid gesture selected please select a valid gesture')
    queryGesture = input()

print('How many gestures should be returned?')
numToReturn = int(input())

# Do Something Here to Find Relevant Gestures

user_choice = 0
while user_choice != 3:
    print("Displaying Relevant Gestures")
    for idx, gesture in enumerate(relevantGestures, 1):
        print(f"{idx}. {gesture}")
    print("\nPick an option:\n1. Give Feedback\n2. Re-run Query\n3. Quit\n")
    user_choice = input()
    if user_choice == 1:
        print("\nSelect the result to give feedback on")
        chosenGesture = input()
        print("\nOn a scale from 1-5 how relevant is this gesture with 5 being very relevant and 1 being completely irrelevant?")
    elif user_choice == 2:
        print("Re-Running the Query with the new feedback...")
        # TODO: Re-run the query with new parameters
    elif user_choice == 3:
        print("Quit Chosen")
    else:
        print("Invalid User Choice!")
print("\nExiting.")
        
    
    