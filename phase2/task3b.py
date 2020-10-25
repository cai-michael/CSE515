import task3_util as util
from task2 import options
import numpy as np
import os
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

    # Perform PCA
    print("Found Gesture-Gesture Similarity Matrix Performing PCA")
    model = decomposition.NMF(n_components=p, max_iter=10000)
    nmfDecomp = model.fit(similarityMatrix)
    
    # Find top-p principle components
    basisVectors = nmfDecomp.components_

    # Find the contributions of each gesture to each basis vectors
    scores = []
    for i in range(p):
        rankedScoresForOneComponent = []
        latentComponentContributions = basisVectors[i]
        for gesture, contribution in zip(gestureIndexes, latentComponentContributions):
            rankedScoresForOneComponent.append((gesture, abs(contribution)))
        rankedScoresForOneComponent.sort(key=lambda pair: pair[1], reverse=True)
        scores.append(rankedScoresForOneComponent)
    
    # Make sure the output directory exists
    working_dir = os.getcwd()
    folder_name = 'principal_components'
    file_name = 'b_components'
    if (not folder_name in os.listdir(working_dir)):
	    os.mkdir(working_dir + '/' + folder_name)

    # Print the results and write to output file
    with open(f'{folder_name}/{file_name}', 'w') as f:
        for index, i in enumerate(scores):
            print(f"Principal Component {index + 1} Similarity Scores:")
            #f.write(f"Principal Component {index + 1} Similarity Scores:\n")
            print("Gesture\t|\tScore")
            for j in i:
                print(f'{j[0]}\t|\t{j[1]}')
                f.write(f'{index}\t|\t{j[0]}\t|\t{j[1]}')
                f.write("\n")
            print("\n")