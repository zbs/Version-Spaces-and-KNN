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
    top_ten_users = sorted_users_by_similarity[:10]
    ranking_vector = calculate_ranking_vector(user, top_ten_users, weighted)
    return get_precision_at_ten(ranking_vector)

if __name__ == '__main__':
    pass