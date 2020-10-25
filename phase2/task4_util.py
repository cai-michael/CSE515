import numpy as np
import random

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