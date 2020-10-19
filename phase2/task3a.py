import task3_util as util
from task2 import options
import numpy as np

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
    u, s, v = np.linalg.svd(similarityMatrix)

    basicVectors = u[:,:p]
    eigenValues = s[:p]

    # Find top-p principle components
    print("something")
