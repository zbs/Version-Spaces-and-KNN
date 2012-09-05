from User import User
'''
Created on Sep 3, 2012

@author: zach

Considerations:
    - After original sorting by similarity, store the similarity per user for future use
'''
TRAIN = '../user_train.txt'
TEST = '../user_test.txt'
MAPPING = '../song_mapping.txt'


def get_users():
    with open(TRAIN) as fp:
        train_text = fp.read()
    return map(lambda x: User(x), train_text.split('\n'))

def sort_users_by_similarity(user, all_users, similarity_metric):
    cmp_funct = user.get_cmp_funct(similarity_metric)
    # Exclude first since it will always be the original user
    return sorted(all_users, cmp=cmp_funct)[1:]
    
def calculate_ranking_vector(user, top_ten_users, weight):
    pass

def get_precision_at_ten(ranking_vector):
    pass

def run_knn(k, weighted, similarity_metric, user, artist=None):
    all_users = get_users()
    sorted_users_by_similarity = sort_users_by_similarity(user, all_users, similarity_metric)
    top_k_users = sorted_users_by_similarity[:10]
    ranking_vector = calculate_ranking_vector(user, top_k_users, weighted)
    return get_precision_at_ten(ranking_vector)

def euclidean_distance(user1_songs, user2_songs):
    
    total = 0
    user_dict = dict([])
    
    for song in user1_songs:
        user_dict[song] = user1_songs[song]
        
    for song in user2_songs:
        if song in user_dict:
            user_dict[song] = user_dict[song] - user2_songs[song]
        else:
            user_dict[song] = user2_songs[song]
            
    for song in user_dict:
        total += user_dict[song]**2
                
            
        
        
    return 1. / total**(1./2.)

def dot_product(user1_songs, user2_songs):
    song_intersection = set.intersection(set(user1_songs.keys()), set(user2_songs.keys()))
    product = 0
    for song in song_intersection:
        product += user1_songs[song] * user2_songs[song]
        
    return product

def cos_distance(user1_songs, user2_songs):
    return dot_product(user1_songs, user2_songs) / (magnitude(user1_songs) * magnitude(user2_songs))
    #return (magnitude(user1_songs) * magnitude(user2_songs))
    
def magnitude(vector):
    return sum(map(lambda x: x**2, vector.values())) ** (1./2.)
     
            
            
            
            
              
    

if __name__ == '__main__':
    pass