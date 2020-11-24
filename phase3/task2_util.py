import pandas as pd
import general_util as util
import os
import numpy as np

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

# Data structure for storing node values inside a Decision Tree
class Node:
    def __init__(self, prediction):
        self.feature_index = 0
        self.threshold = 0
        self.left = None
        self.right = None
        self.prediction = prediction

# expects a numpy arr for both params
def fit_decision_tree(independent_dataset, dependent_dataset):
    no_of_classes = len(set(dependent_dataset))
    no_of_features = independent_dataset.shape[1] # choose the columns, not the rows
    tree = develop_tree(0, no_of_classes, no_of_features, independent_dataset, dependent_dataset)
    return tree

def predict(tree, input_data):
    results = []
    for input in input_data:
        results.append(predict_on_tree(tree, input))
    return results

def predict_on_tree(tree, input):
        while tree.left:
            # if it matches the criterion, explore left subtree
            if input[tree.feature_index] < tree.threshold:
                tree = tree.left
            else:
            # else explore right subtree
                tree = tree.right
        # return the prediction of the leaf node
        return tree.prediction

def develop_tree(depth, no_of_classes, no_of_features, independent_dataset, dependent_dataset):
    best_prediction_size =  np.argmax(determine_size_of_class(dependent_dataset, no_of_classes))
    node = Node(prediction=best_prediction_size)
    if depth < 50000:
        idx, threshold_pivot = determine_split(independent_dataset, dependent_dataset, no_of_classes, no_of_features)
        if idx is not None:
            indices_left = independent_dataset[:, idx] < threshold_pivot
            X_left, y_left = independent_dataset[indices_left], dependent_dataset[indices_left]
            X_right, y_right = independent_dataset[~indices_left], dependent_dataset[~indices_left]
            # Prepare the sub node on this tree
            node.feature_index = idx
            node.threshold = threshold_pivot
            left_subtree = develop_tree(depth + 1, no_of_classes, no_of_features, X_left, y_left,)
            node.left = left_subtree
            right_subtree = develop_tree(depth + 1, no_of_classes, no_of_features, X_right, y_right)
            node.right = right_subtree
    return node

def determine_split(independent_dataset, dependent_dataset, no_of_classes, no_of_features):
        if dependent_dataset.size <= 1:
            # return left and right subtrees as null
            return None, None
        unique_classes = determine_size_of_class(dependent_dataset, no_of_classes)
        best_gini = 1.0 - sum((n / dependent_dataset.size) ** 2 for n in unique_classes)
        best_idx, best_thr = None, None
        for idx in range(no_of_features):
            thresholds, classes = zip(*sorted(zip(independent_dataset[:, idx], dependent_dataset)))
            num_left = [0] * no_of_classes
            num_right = unique_classes.copy()
            for i in range(1, dependent_dataset.size):
                c = classes[i - 1]
                num_left[c] += 1
                num_right[c] -= 1
                gini_left = 1.0 - sum(
                    (num_left[class_c] / i) ** 2 for class_c in range(no_of_classes)
                )
                gini_right = 1.0 - sum(
                    (num_right[class_c] / (dependent_dataset.size - i)) ** 2 for class_c in range(no_of_classes)
                )
                gini = (i * gini_left + (dependent_dataset.size - i) * gini_right) / dependent_dataset.size
                if thresholds[i] == thresholds[i - 1]:
                    continue
                if gini < best_gini:
                    best_gini = gini
                    best_idx = idx
                    best_thr = (thresholds[i] + thresholds[i - 1]) / 2
        return best_idx, best_thr


def determine_size_of_class(labels, no_of_classes):
    return [np.sum(labels == class_c) for class_c in range(no_of_classes)]

