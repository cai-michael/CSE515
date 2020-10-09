from query import determineMostSimilarGestures
folder = 'data'
files = ['test1.csv', 'test2.csv', 'test3.csv', 'test4.csv', 'test5.csv', 'test6.csv']
choice = [1, 2, 3]
name = ['TF', 'TF-IDF', 'TF-IDF2']

f = open('outputs/queryResults.txt', 'a')
for k in files:
    for j in choice:
        similarGestures = determineMostSimilarGestures(folder, k, j)
        
        f.write(k + ' ' + name[j - 1] + '\n')
        f.write('These are the most similar gestures to your choice:\n')
        f.write('Rank\t|\tGesture\t|\tSimilarity Score\n')
        for i in range(10):
            f.write(str(str(i + 1) + '\t|\t' + similarGestures[i][0]) + '\t|\t%.5f\n' % similarGestures[i][1]) 
    
f.close()