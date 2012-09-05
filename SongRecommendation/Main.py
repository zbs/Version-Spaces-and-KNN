from User import User
import heapq
'''
Created on Sep 3, 2012

@author: zach

Considerations:
    - After original sorting by similarity, store the similarity per user for future use
    - Cache similarities between users
    - 2) Feel free to use a "k-largest numbers in list" routine to increase the efficiency of finding the k-nearest neighbors. Calculate the similarities to all other users for a given user and then process the unsorted list with such a function instead of just sorting the whole list and taking the first k entries. Python has heapq.nlargest() for this, for example. This can get you the k-nearest neighbors in something like O(nlogk) time instead of O(nlogn), which is a savings of roughly half the run-time when k = 3 or of about 15% when k = 1000.
    
'''
TRAIN = '../data/user_train.txt'
TEST = '../data/user_test.txt'
MAPPING = '../data/song_mapping.txt'

def get_users():
    with open(TRAIN) as fp:
        train_text = fp.read().strip()
    return map(lambda x: User(x), train_text.split('\n'))

def sort_users_by_similarity(user, all_users, similarity_metric):
    cmp_funct = user.get_cmp_funct(similarity_metric)
    # Exclude first since it will always be the original user
    return sorted(all_users, cmp=cmp_funct)[1:]

def get_top_k_users(user, all_users, k, similarity_metric):
    similarity_funct = user.get_similarity_funct(similarity_metric)
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
                similarity = similarity_metric(user.songs, top_user.songs)
                modified_song_count *= similarity
                similarity_total += similarity
                
            if song_id not in sums:
                sums[song_id] = modified_song_count
            else:
                sums[song_id] += modified_song_count
    for song_id in sums:
        if weighted:
            sums[song_id] /= similarity_total
        else:
            sums[song_id] /= k
    return sums
        
def get_precision_at_ten(top_ten_songs, liked_songs):
    return len(filter(lambda x: x in liked_songs, top_ten_songs))/len(top_ten_songs)


def get_top_ten_songs(ranking_vector):
    heapq.nlargest(10, ranking_vector, key=lambda x: ranking_vector[x])


def run_knn_per_user(k, weighted, similarity_metric, user, users, liked_songs, get_top_songs=True):
    all_users = users
    top_k_users = get_top_k_users(user, all_users, k, similarity_metric)
    ranking_vector = calculate_ranking_vector(user, top_k_users, k, similarity_metric, weighted)
    top_ten_songs = get_top_ten_songs(ranking_vector)
    if not get_top_songs:
        return get_precision_at_ten(top_ten_songs, liked_songs)
    else:
        # Send back top ten songs from collection and from ranked vector
        pass
    

def get_liked_songs():
    with open(TEST) as fp:
        liked_string = fp.read().strip()
    def parse_line(liked_line):
        user_id, song_string = liked_line.split(' - ')
        return (user_id, set(song_string.split(' ')))
    return dict(map(parse_line, liked_string.split('\n')))


def get_song_mappings():
    pass


def run_knn(k, weighted, similarity_metric_index, user=None, artist=None):
    # Replace None with actual functions
    similarity_metric = {0: None, 1:None, 2:None}[similarity_metric_index]
    
    all_users = get_users()
    liked_songs = get_liked_songs()
    song_mappings = get_song_mappings()
    
    if user != None:
        def get_user_precision(user):
            return run_knn_per_user(k, weighted, similarity_metric, user, 
                                    all_users, liked_songs, False)
        # Average precision
        return sum(map(get_user_precision, all_users))/len(all_users)
    elif artist != None:
        pass
    else:
        pass
        

if __name__ == '__main__':
    pass