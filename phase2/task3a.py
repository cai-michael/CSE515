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
    
    if option in [2,3,4,5]:
        top_k_input = int(input('How many top-k components did you specify during Task 1?  (e.g. 1, 2, etc.): '))

    vector_model = None

    if option < 6:
        vector_model = input('Please select a vector model (TF/TF-IDF): ')
        while vector_model not in { 'TF', 'TF-IDF' }:
            print('Invalid vector model. Please try again.')
            vector_model = input('Please select a vector model (TF/TF-IDF): ')
    
    similarityMatrix, gestureIndexes = util.createSimilarityMatrix(vector_model, option, top_k_input)

    # Perform SVD
    print("Found Gesture-Gesture Similarity Matrix Performing SVD")
    model = decomposition.TruncatedSVD(n_components=p)
    svdDecomp = model.fit(similarityMatrix)

    # Find top-p principle components
    basisVectors = svdDecomp.components_

    # Find the contributions of each gesture to each basis vectors
    scores = []
    for i in range(p):
        rankedScoresForOneComponent = []
        latentComponentContributions = basisVectors[i]
        for gesture, contribution in zip(gestureIndexes, latentComponentContributions):
            rankedScoresForOneComponent.append((gesture, abs(contribution)))
        rankedScoresForOneComponent.sort(key=lambda pair: pair[1], reverse=True)
        scores.append(rankedScoresForOneComponent)
    
    # Print out results
    for index, i in enumerate(scores):
        print(f"Principal Component {index + 1} Similarity Scores:")
        print("Gesture\t|\tScore")
        for j in i:
            print(f'{j[0]}\t|\t{j[1]}')
        print("\n")