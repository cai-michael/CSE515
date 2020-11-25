The tasks for this project were implemented as separate Python scripts:
	task0.py
	task1.py
	task2.py
	task3.py
	task4.py
	task5.py
	task6.py

But the only tasks which actually need to be run in the command line are
Task 1 – task1.py
Task 2 – task2.py
Task 3 – task3.py
Task 6 – task6.py (will include task 4 and task 5 running)
	
The above python scripts should be executed in numerical order to satisfy data dependencies.
To execute a file, use the command:
	python3 <file_name>

The programs were intended to be run using Python version 3.8.5 or higher.
Required Libraries:
	Python 3.8.5
	math
	numpy
	os
	shutil
	pandas
	pprint
	matplotlib


task0.py
This program performs preliminary processing of the data to make it usable for later tasks, converts the *.csv gesture data into *.wrd gesture dictionaries in the folder wrd_data, and produces a similarity graph.py
	Inputs:
	data - the name of the folder containing the component folders of *.csv data
	r - the resolution used for quantization (positive integer)
	w - the window size used for SAX (positive integer)
	s - the shift length used for SAX (positive integer)
	distance metric (negative euclidean or dot product) - used to build the gesture-gesture similarity matrix

task1.py
This program runs the PPR algorithm on the similarity_matrix.txt outputted from Task 0.

	Inputs:
	k - Number of outgoing edges
	m - Number of dominant gestures
	n - A Comma separated list of seed gestures

task2.py
This program will clasify gestures using KNN, Decision Tree Classifer, or PPR-based classifier, and output the results.

	Inputs:
	A classifier (one of 3 options)
	A range of gesture labels for each class

task3.py
This program will generate a LSH data structure and hashing functions for gesture dataset from Task 0's output. 

	Inputs:
	L - number of layers
	k - number of hash functions per layer
	Vector model representation (TF or TF-IDF)
	t - gestures to return

task6.py
This program will provide an interface for the user to run a query. The user will be prompted with the same prompts as task3.py, and additionally
given the option to give relevance feedback and apply that feedback in realtime on the query. 

Inputs
 - Same inputs as in task 3
 - Feedback model to pick (probabilistic relevance feedback or classifier-based feedback)
 - Option to given feedback, apply weights, or Quit