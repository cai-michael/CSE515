import task3_util as util
from task2 import options
from task4_util import kmeans

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
        while vector_model not in {'TF', 'TF-IDF'}:
            print('Invalid vector model. Please try again.')
            vector_model = input('Please select a vector model (TF/TF-IDF): ')
    
    top_k_input = None
    if option in [2,3,4,5]:
        top_k_input = int(input('How many top-k components did you specify during Task 1? (e.g. 1, 2, etc.): '))

    similarityMatrix, gestureIndexes = util.createSimilarityMatrix(vector_model, option, top_k_input)

    labels, points, centroids = kmeans(similarityMatrix, p)

    # Print out results
    print(f"K-Means Clustering Results (sorted by gesture):")
    print("Gesture\t|\tCluster")
    for i in range(len(labels)):
        print(f'{gestureIndexes[i]}\t\t|\t{labels[i]}')
    print("\n")

    indexes = list(range(len(labels)))
    indexes.sort(key=labels.__getitem__)

    # Print out results
    print(f"K-Means Clustering Results (sorted by cluster):")
    print("Gesture\t|\tCluster")
    for i in indexes:
        print(f'{gestureIndexes[i]}\t\t|\t{labels[i]}')
    print("\n")
