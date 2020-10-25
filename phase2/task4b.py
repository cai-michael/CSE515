import os

# Main
if __name__ == '__main__':
    gestureHighestDegreeOfMembershipDictionary = {}
    directory = "principal_components"
    # Read in b_components file from directory
    for component_file in os.listdir(directory):
        if "b" in component_file:
            print("Reading in "  + component_file + " file from Task 3b output \n")
            with open(directory + "/" + component_file) as f:
                for line in f:
                    gesture_component_combination = line.split("|")
                    p_component = int(gesture_component_combination[0])
                    gesture = int(gesture_component_combination[1])
                    similarity_score = float(gesture_component_combination[2])
                    currentComponentContributionPair = (p_component, similarity_score)
                    # Create gesture dictionary with highest degree of membership
                    if gestureHighestDegreeOfMembershipDictionary.get(gesture) != None:
                        maximumComponentContributionPair = gestureHighestDegreeOfMembershipDictionary.get(gesture)
                        gestureHighestDegreeOfMembershipDictionary[gesture] = maximumComponentContributionPair if maximumComponentContributionPair[1]\
                            > currentComponentContributionPair[1] else currentComponentContributionPair
                    else:
                        gestureHighestDegreeOfMembershipDictionary[gesture] = currentComponentContributionPair
  
    p = p_component + 1
    # Print results
    print("Partitioning gestures into " + str(p) + " groups based on degree of membership\n")
    for i in range(p):
        print(f"Gestures With Highest Degree of Membership for Principal Component {i + 1}:")
        print("Gesture\t|\tScore")
        for gesture, degreeOfMembershipPair in gestureHighestDegreeOfMembershipDictionary.items():
            if degreeOfMembershipPair[0] == i:
                 print(f'{gesture}\t|\t{degreeOfMembershipPair[1]}')
        print("\n")