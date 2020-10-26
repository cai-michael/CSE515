The tasks for this project were implemented as 10 separate Python scripts:
	task0a.py
	task0b.py
	task1.py
	task2.py
	task3a.py
	task3b.py
	task4a.py
	task4b.py
	task4c.py
	task4d.py
These scripts should be executed in numerical order to satisfy data dependencies.
To execute a file, use the command:
	python <file_name>


The programs were intended to be run using Python version 3.8.5 or higher.
Testing was done on Windows but measures were taken to hopefully ensure Linux compatibility.
Required Libraries:
	numpy
	os
	pathlib
	platform
	sklearn
	sys
	typing


task0a.py
This program converts the *.csv gesture data into *.wrd gesture dictionaries in the folder wrd_data.
Inputs:
	data - the name of the folder containing the component folders of *.csv data
	r - the resolution used for quantization (positive integer)
	w - the window size used for SAX (positive integer)
	s - the shift length used for SAX (positive integer)


task0b.py
This program creates TF and TF-IDF gesture vectors for each gesture in the wrd_data folder.
The results are stored in the folder vector_data.
There are no inputs required for this program.


task1.py
This program extracts the top-k latent semantics from the vector data using a user-specified method.
The results are stored in the folder latent_semantic_data
Inputs:
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use
	method of analysis ('PCA', 'SVD', 'NMF', 'LDA') - the technique to use in finding the latent semantics
	k - the number of latent semantics to extract (positive integer)


task2.py
This program searches the database for the 10 most similar gestures to an input "query" gesture.
The results are listed as "<gesture> | <score>" pairs.
Options 2-5 of task2.py use the latent semantics computed by task1.py, so it is necessary to run task1.py for the
	method of analysis with which you intend to search
Inputs:
	gesture file (no extension) - the name of the gesture file to use as a query for similarity-based ranking
	similarity metric - the id number of the metric with which to search:
		1: dot product
		2: PCA semantics
		3: SVD semantics
		4: NMF semantics
		5: LDA semantics
		6: edit-distance
		7: dynamic time warping distance
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use


task3a.py
This program applies dimensionality reduction via SVD to extract the top-p principal components of a gesture-gesture
	similarity matrix defined using a user-specified similarity metric.
The results are stored in the principal_components folder.
Inputs:
	p - the number of principal components to report (positive integer)
	similarity metric - the id number of the metric to use for gesture-gesture comparison:
		1: dot product
		2: PCA semantics
		3: SVD semantics
		4: NMF semantics
		5: LDA semantics
		6: edit-distance
		7: dynamic time warping distance
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use


task3b.py
This program applies dimensionality reduction via NMF to extract the top-p principal components of a gesture-gesture
	similarity matrix defined using a user-specified similarity metric.
The results are stored in the principal_components folder.
Inputs:
	p - the number of principal components to report (positive integer)
	similarity metric - the id number of the metric to use for gesture-gesture comparison:
		1: dot product
		2: PCA semantics
		3: SVD semantics
		4: NMF semantics
		5: LDA semantics
		6: edit-distance
		7: dynamic time warping distance
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use


task4a.py
This program partitions the gestures into p groups using the principal components extracted by task3a.py.
The results are printed to the screen, component by component, as a list of gestures ranked by their contribution.
There are no inputs required for this program.


task4b.py
This program partitions the gestures into p groups using the principal components extracted by task3b.py.
The results are printed to the screen, component by component, as a list of gestures ranked by their contribution.
There are no inputs required for this program.


task4c.py
This program uses a gesture-gesture similarity matrix to cluster the gestures into p groups using k-means.
The results are printed to the screen as a list of "<gesture> | <cluster_id>" pairs.
Inputs:
	p - the number of groups into which to partition the gestures (positive integer)
	similarity metric - the id number of the metric to use for gesture-gesture comparison:
		1: dot product
		2: PCA semantics
		3: SVD semantics
		4: NMF semantics
		5: LDA semantics
		6: edit-distance
		7: dynamic time warping distance
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use
	k - the number of latent semantics extracted by task1.py (positive integer)


task4d.py
This program uses a gesture-gesture similarity matrix to cluster the gestures into p groups using Laplacian
	spectral clustering.
The results are printed to the screen as a list of "<gesture> | <cluster_id>" pairs.
Inputs:
	p - the number of groups into which to partition the gestures (positive integer)
	similarity metric - the id number of the metric to use for gesture-gesture comparison:
		1: dot product
		2: PCA semantics
		3: SVD semantics
		4: NMF semantics
		5: LDA semantics
		6: edit-distance
		7: dynamic time warping distance
	vector model ('TF', 'TF-IDF') - type of gesture vectors to use
	k - the number of latent semantics extracted by task1.py (positive integer)


Helper files
Several utility files are included containing necessary variables and functions for some of the programs:
	general_util.py
	task0_util.py
	task3_util.py
	task4_util.py
The programs additionally use a file named "user_settings.txt" to share information about the options the user
	has chosen.

