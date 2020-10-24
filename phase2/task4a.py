import task3_util as util
from task2 import options
import numpy as np
from sklearn import decomposition

# Main
if __name__ == '__main__':
    # Load arguments
    p = int(input('How many principle components to return: '))

    # List options
    print('Options:')
    for option_number, (option_name, _, _) in options.items():
        print(f'{option_number}. {option_name}')

    option = int(input('Please select an option: '))
    while option not in options:
        print('Invalid option. Please try again.')
        option = int(input('Please select an option: '))

    vector_model = None

    if option < 6:
        vector_model = input('Please select a vector model (TF/TF-IDF): ')
        while vector_model not in { 'TF', 'TF-IDF' }:
            print('Invalid vector model. Please try again.')
            vector_model = input('Please select a vector model (TF/TF-IDF): ')
    
    similarityMatrix, gestureIndexes = util.createSimilarityMatrix(vector_model, option)

    # Perform SVD
    print("Found Gesture-Gesture Similarity Matrix Performing SVD\n")
    model = decomposition.TruncatedSVD(n_components=p)
    svdDecomp = model.fit(similarityMatrix)
    # Find top-p principle components
    basisVectors = svdDecomp.components_

    # Find the contributions of each gesture to each basis vectors
    gestureHighestDegreeOfMembershipDictionary = {}
    for i in range(p):
        latentComponentContributions = basisVectors[i]
        for gesture, contribution in zip(gestureIndexes, latentComponentContributions):
            currentComponentContributionPair = (i, abs(contribution))
            if gestureHighestDegreeOfMembershipDictionary.get(gesture) != None:
                maximumComponentContributionPair = gestureHighestDegreeOfMembershipDictionary.get(gesture)
                gestureHighestDegreeOfMembershipDictionary[gesture] = maximumComponentContributionPair if maximumComponentContributionPair[1]\
                    > currentComponentContributionPair[1] else currentComponentContributionPair
            else:
                gestureHighestDegreeOfMembershipDictionary[gesture] = currentComponentContributionPair
   
    # Print
    print("Partitioning gestures into " + str(p) + " groups based on degree of membership")
    for i in range(p):
        print(f"Gestures With Highest Degree of Membership for Principal Component {i + 1}:")
        print("Gesture\t|\tScore")
        for gesture, degreeOfMembershipPair in gestureHighestDegreeOfMembershipDictionary.items():
            if degreeOfMembershipPair[0] == i:
                 print(f'{gesture}\t|\t{degreeOfMembershipPair[1]}')
        print("\n")