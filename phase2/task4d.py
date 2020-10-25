import random
import task3_util as util
from task2 import options
import numpy as np

def kmeans(data, k):
    threshold = .0001
    max_iter = 200

    # set k centroids
    centroids = random.sample(list(data), k)

    for iter in range(max_iter):
        labels = []
        points = {}

        for i in range(len(data)):
            dists = []
            for j in range(len(centroids)):
                dists.append(np.linalg.norm(data[i] - centroids[j]))
            label = dists.index(min(dists))
            labels.append(label)
            if label not in points:
                points[label] = []
            points[label].append(data[i])

        prev_centroids = np.array(centroids)

        for i in range(len(points)):
            centroids[i] = np.average(points[i], axis=0)

        exit_loop = True
        for i in range(k):
            if np.sum((centroids[i] - prev_centroids[i]) / prev_centroids[i] * 100.0) > threshold:
                exit_loop = False

        if exit_loop:
            break

    return labels, points, centroids

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

    similarityMatrix, gestureIndexes = util.createSimilarityMatrix(vector_model, option)

    # weighted similarity matrix
    for i in range(len(similarityMatrix)):
        for j in range(len(similarityMatrix[i])):
            if similarityMatrix[i][j] < 0:
                similarityMatrix[i][j] = 0

    # degree matrix
    degreeMatrix = []
    for vertex in similarityMatrix:
        degreeMatrix.append(sum(vertex))

    # unnormalized laplacian matrix
    laplacianMatrix = np.subtract(degreeMatrix, similarityMatrix)

    eigenValues, eigenVectors = np.linalg.eig(laplacianMatrix)
    eigenVectors = eigenVectors[:, np.argsort(eigenValues)]
    eigenValues = eigenValues[np.argsort(eigenValues)]

    labels, points, centroids = kmeans(eigenVectors[:, 1:p], p)

    print(f"Laplacian-based Spectral Clustering Results (sorted by gesture):")
    print("Gesture\t|\tCluster")
    for i in range(len(labels)):
        print(f'{gestureIndexes[i]}\t\t|\t{labels[i]}')
    print("\n")

    indexes = list(range(len(labels)))
    indexes.sort(key=labels.__getitem__)

    # Print out results
    print(f"Laplacian-based Spectral Clustering Results (sorted by cluster):")
    print("Gesture\t|\tCluster")
    for i in indexes:
        print(f'{gestureIndexes[i]}\t\t|\t{labels[i]}')
    print("\n")
