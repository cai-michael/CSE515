from task3_util import load_vector, load_vectors, LSH
from pprint import pprint


if __name__ == '__main__':
    L = int(input('Please enter the number of layers L: '))
    k = int(input('Please enter the number of hashes per layer k: '))
    vector_model = input('Please enter a vector model (TF/TF-IDF): ')

    # Load vectors from vector_data folder
    vectors, vector_ids = load_vectors(vector_model)

    # Initialize LSH index structure
    lsh = LSH(L, k, vectors, vector_ids)

    #pprint(lsh.tables)

    gesture_id = input('Please enter a gesture id (e.g. 1, 249, 559, etc.): ')

    t = int(input('Please enter t: '))

    query = load_vector(vector_model, gesture_id)

    # Find t most similar gestures
    top_t, no_buckets, no_unique, overall_no = lsh.find_t_most_similar(query, t)

    print('No. of buckets searched: ', no_buckets)
    print('No. of unique gestures considered: ', no_unique)
    print('Overall no. of gestures considered: ', overall_no)

    print(f'Top {t} most similar gestures:')
    for index, (gesture_id, distance) in enumerate(top_t):
        print(f'{index + 1}.\t{gesture_id}\t(distance={distance})')
