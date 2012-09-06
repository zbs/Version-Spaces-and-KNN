from User import User
import heapq
import sys
import cProfile
import pickle
'''
Created on Sep 3, 2012

@author: zach

Considerations:
    - After original sorting by similarity, store the similarity per user for future use
    - Cache similarities between users
    - 2) Feel free to use a "k-largest numbers in list" routine to increase the efficiency of finding the k-nearest neighbors. Calculate the similarities to all other users for a given user and then process the unsorted list with such a function instead of just sorting the whole list and taking the first k entries. Python has heapq.nlargest() for this, for example. This can get you the k-nearest neighbors in something like O(nlogk) time instead of O(nlogn), which is a savings of roughly half the run-time when k = 3 or of about 15% when k = 1000.
    
'''
REDUCED = False

REDUCED_TRAIN = '../reduced_data/user_train_reduced.txt'
REDUCED_TEST = '../reduced_data/user_test_reduced.txt'

TRAIN = REDUCED_TRAIN if REDUCED else '../data/user_train.txt'
TEST = REDUCED_TEST if REDUCED else '../data/user_test.txt'

MAPPING = '../data/song_mapping.txt'

CACHES = {0:'EUCLIDEAN_CACHE', 1:'DOT_CACHE', 2:'COSINE_CACHE'}
similarity_cache = {}

def get_users():
    with open(TRAIN) as fp:
        train_text = fp.read().strip()
    return map(lambda x: User(x), train_text.split('\n'))

def get_top_k_users(user, all_users, k, similarity_metric, is_user_generated=False):
    similarity_funct = user.get_similarity_funct(similarity_metric)
    # Discount the first user since it is the same as the one being
    # compared against
    if not is_user_generated:
        return heapq.nlargest(k+1, all_users, similarity_funct)[1:]
    else:
        return heapq.nlargest(k, all_users, similarity_funct)
    
def calculate_ranking_vector(user, top_k_users, k, similarity_metric, weighted):
    similarity_total = 0
    sums = {}
    for top_user in top_k_users:
        for song_id in top_user.songs:
            if song_id in user.songs:
                # This ignores all songs in the users collection,
                # as per the instructions
                continue
            
            modified_song_count = top_user.songs[song_id]
            
            if weighted:
                similarity = similarity_metric(user, top_user)
                modified_song_count *= similarity
                similarity_total += similarity
                
            if song_id not in sums:
                sums[song_id] = modified_song_count
            else:
                sums[song_id] += modified_song_count
    for song_id in sums:
        if weighted:
            sums[song_id] /= float(similarity_total)
        else:
            sums[song_id] /= float(k)
    return sums
        
def get_precision_at_ten(top_ten_songs, liked_songs):
    return len(filter(lambda x: x in liked_songs, top_ten_songs))/float(len(top_ten_songs))

def get_top_ten_songs(ranking_vector):
    return heapq.nlargest(10, ranking_vector, key=lambda x: ranking_vector[x])

def run_knn_per_user(k, weighted, similarity_metric, user, users, liked_songs, get_top_songs=True):
    all_users = users
    top_k_users = get_top_k_users(user, all_users, k, similarity_metric)
    ranking_vector = calculate_ranking_vector(user, top_k_users, k, similarity_metric, weighted)
    top_ten_songs = get_top_ten_songs(ranking_vector)
    precision = get_precision_at_ten(top_ten_songs, liked_songs)
    if not get_top_songs:
        return precision
    else:
        top_ten_collection_songs = heapq.nlargest(10, user.songs, lambda x: user.songs[x])
        return (precision, top_ten_songs, top_ten_collection_songs)

def get_liked_songs():
    with open(TEST) as fp:
        liked_string = fp.read().strip()
    def parse_line(liked_line):
        user_id, song_string = liked_line.split(' - ')
        return (user_id, set(song_string.split(' ')))
    # Format is x = dict, x[id] = set of song id strings
    return dict(map(parse_line, liked_string.split('\n')))
#.573
def get_artist_songs(artist):
    with open(MAPPING) as fp:
        mapping_pieces = fp.read().split('\n')
    return map(lambda x: x.split('\t')[0], filter(lambda x: x.find(artist) != -1, mapping_pieces))

def get_relevant_songs(artist):
    pass

def get_song_mappings():
    with open(MAPPING) as fp:
        text = fp.read()
    mapping_lines = map(lambda x: x.split('\t'), text.split('\n'))
    return dict(map(lambda x: (x[0], x[1:]), mapping_lines))

def run_knn(k, weighted, similarity_metric_index, user_id=None, artist=None):
    # Replace None with actual functions
    similarity_metric = cached_similarity(similarity_metric_index, True)
    
    mappings = get_song_mappings()
    all_users = get_users()
    liked_songs = get_liked_songs()
    
    if user_id != None:
        user = filter(lambda x: x.id == user_id, all_users)[0]
        return run_knn_per_user(k, weighted, similarity_metric, user, 
                                    all_users, liked_songs, True)
    elif artist != None:
        artist_songs = get_artist_songs(artist)

        def f(x):
            return (x,1)
        generated_user = User(user_id=-1, user_songs=dict(map(f, artist_songs)))

        top_k_users = get_top_k_users(generated_user, all_users, k, similarity_metric, is_user_generated=True)
        ranking_vector = calculate_ranking_vector(generated_user, top_k_users, k, similarity_metric, weighted)
        top_ten_songs = get_top_ten_songs(ranking_vector)
        return top_ten_songs
    else:
        def get_user_precision(user):
            if user.id % 100 == 0:
                print user.id
                
            return run_knn_per_user(k, weighted, similarity_metric, user, 
                                    all_users, liked_songs, False)
        # Average precision
        avg_precision = sum(map(get_user_precision, all_users))/float(len(all_users))
        
        cache_name = CACHES[similarity_metric_index]
        if not does_file_exist(cache_name):
            pickle.dump(similarity_cache, open(cache_name, 'w'))
        return avg_precision

def euclidean_distance(user1_songs, user2_songs):
    user_dict = {}
    
    for song in user1_songs:
        user_dict[song] = user1_songs[song]
        
    for song in user2_songs:
        if song in user_dict:
            user_dict[song] = user_dict[song] - user2_songs[song]
        else:
            user_dict[song] = user2_songs[song]
    
    total = sum(map(lambda x: user_dict[x]**2, user_dict))
    if total == 0:
        return sys.maxint
    return 1. / total

def dot_product(user1_songs, user2_songs):
    song_intersection = set.intersection(set(user1_songs.keys()), set(user2_songs.keys()))
    product = 0
    for song in song_intersection:
        product += user1_songs[song] * user2_songs[song]
        
    return product

def cached_similarity(similarity_metric_index, external_cache=False):
#    {0: euclidean_distance, 1:dot_product, 2:cos_distance}[similarity_metric_index]
        if external_cache:
            global similarity_cache
            pickled_file = CACHES[similarity_metric_index]
            if does_file_exist(pickled_file):
                similarity_cache = pickle.load(open(pickled_file))
        
        similarity_metric = {0: euclidean_distance, 1:dot_product, 2:cos_distance}[similarity_metric_index]
        def helper(user1, user2):
            global similarity_cache
            if (user1.id, user2.id) in similarity_cache:
                return similarity_cache[(user1.id, user2.id)]
            elif (user2.id, user1.id) in similarity_cache:
                return similarity_cache[(user2.id, user1.id)]
            else:
                similarity = similarity_metric(user1.songs, user2.songs)
                similarity_cache[(user1.id, user2.id)] = similarity
                return similarity
        return helper

def cos_distance(user1_songs, user2_songs):
    return dot_product(user1_songs, user2_songs) / (magnitude(user1_songs) * magnitude(user2_songs))
    #return (magnitude(user1_songs) * magnitude(user2_songs))
    
def does_file_exist(filename):
    try:
        with open(filename) as f: pass
    except IOError:
        return False
    return True

def magnitude(vector):
    return sum(map(lambda x: x**2, vector.values())) ** (1./2.)
     
if __name__ == '__main__':
    run_knn(1, False, 0, None, None)
#    run_knn(10, False, 0, None, "Usher")
#    cProfile.run('run_knn(250, False, 0, None, None)')
