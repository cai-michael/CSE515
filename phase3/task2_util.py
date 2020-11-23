import pandas as pd
import general_util as util
import os

# return the option that occurs most, or the earlier one if there's a tie
def majority_vote(votes):
	counts = {}
	for k in votes:
		if(not k in counts):
			counts[k] = votes.count(k)
	cvalues = list(counts.values())
	return list(counts.keys())[cvalues.index(max(cvalues))]



# expresses numeric data_files as a list of strings; hard to explain
# don't call this function unless you're in the know!
def numeric_data_files_to_pretty_string(data_files):
	numeric = filter(lambda a : a.isnumeric(), data_files)
	numeric = list(map(int, numeric))
	
	# horrible list comprehension (but effective)
	numeric = [':' if (ind > 0) and (ind < len(numeric)-1) and
			(numeric[ind] == numeric[ind-1]+1) and (numeric[ind] == numeric[ind+1]-1)
		else str(numeric[ind])
		for ind in range(len(numeric))]
	
	numeric = str(numeric)[1:-1].replace("'",'').replace(' ','')
	numeric = numeric.replace(':,',':').replace(',:',':')
	while('::' in numeric):
		numeric = numeric.replace('::',':')
	numeric = numeric.split(',')
	return numeric

# expresses the data_files compactly using ranges
def data_files_to_pretty_string(data_files, give_overview=True):
	families = {}
	for f in data_files:
		prefix = f.split('_')[0]
		if(not prefix in families):
			families[prefix] = []
		families[prefix].append(f)
	
	for k in families:
		families[k] = util.sortFileNames(families[k])
	
	keylist = util.sortFileNames(list(families.keys()))
	
	result = []
	if(give_overview):
		overview = numeric_data_files_to_pretty_string(keylist)
		for s in overview:
			if(':' in s):
				s = s.split(':')
				result.append(families[s[0]][0] + ':' + families[s[1]][-1])
			else:
				result.append(s)
	
	for k in keylist:
		if(len(families[k]) > 1):
			result.append(families[k][0] + ':' + families[k][-1])
		else:
			result.append(families[k][0])
	
	result = str(result)[1:-1].replace("'",'').replace(' ','')
	result = result.replace(':,',':').replace(',:',':')
	return result.replace(',',', ')



# A helper function to read the sample_training_labels excel file.
# Returns a mapping for a gesture to its label
def get_gesture_label_mapping(filename='sample_training_labels.xlsx'):
    dict_mapping = {}
    working_dir = os.getcwd()
    mapping_file = working_dir + util.SLASH + filename
    df = pd.read_excel(mapping_file, header=None)
    for idx, row in df.iterrows():
        # set key as gestureId and value as the label
        dict_mapping[row.iloc[0]] = row.iloc[1]
    
    return dict_mapping

"""Implementation of the CART algorithm to train decision tree classifiers."""
import numpy as np

class Node:
    def __init__(self, predicted_class):
        self.predicted_class = predicted_class
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None

class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.n_classes_ = len(set(y))
        self.n_features_ = X.shape[1]
        self.tree_ = self._grow_tree(X, y)

    def predict(self, X):
        return [self._predict(inputs) for inputs in X]

    def _best_split(self, X, y):
        m = y.size
        if m <= 1:
            return None, None
        num_parent = [np.sum(y == c) for c in range(self.n_classes_)]
        best_gini = 1.0 - sum((n / m) ** 2 for n in num_parent)
        best_idx, best_thr = None, None
        for idx in range(self.n_features_):
            thresholds, classes = zip(*sorted(zip(X[:, idx], y)))
            num_left = [0] * self.n_classes_
            num_right = num_parent.copy()
            for i in range(1, m):
                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                gini_left = 1.0 - sum(
                    (num_left[x] / i) ** 2 for x in range(self.n_classes_)
                )
                gini_right = 1.0 - sum(
                    (num_right[x] / (m - i)) ** 2 for x in range(self.n_classes_)
                )
                gini = (i * gini_left + (m - i) * gini_right) / m
                if thresholds[i] == thresholds[i - 1]:
                    continue
                if gini < best_gini:
                    best_gini = gini
                    best_idx = idx
                    best_thr = (thresholds[i] + thresholds[i - 1]) / 2
        return best_idx, best_thr

    def _grow_tree(self, X, y, depth=0):
        num_samples_per_class = [np.sum(y == i) for i in range(self.n_classes_)]
        predicted_class = np.argmax(num_samples_per_class)
        node = Node(predicted_class=predicted_class)
        if depth < self.max_depth:
            idx, thr = self._best_split(X, y)
            if idx is not None:
                indices_left = X[:, idx] < thr
                X_left, y_left = X[indices_left], y[indices_left]
                X_right, y_right = X[~indices_left], y[~indices_left]
                node.feature_index = idx
                node.threshold = thr
                node.left = self._grow_tree(X_left, y_left, depth + 1)
                node.right = self._grow_tree(X_right, y_right, depth + 1)
        return node

    def _predict(self, inputs):
        node = self.tree_
        while node.left:
            if inputs[node.feature_index] < node.threshold:
                node = node.left
            else:
                node = node.right
        return node.predicted_class