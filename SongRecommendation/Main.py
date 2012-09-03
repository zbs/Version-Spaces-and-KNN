'''
Created on Sep 3, 2012

@author: zach

Considerations:
    - After original sorting by similarity, store the similarity per user for future use
'''
def run_knn(k, weighted, similarity_metric, user, artist=None):
    all_users = get_users()
    sorted_users_by_similarity = sort_users_by_similarity(user, all_users, similarity_metric)
    top_ten_users = sorted_users_by_similarity[:10]
    ranking_vector = calculate_ranking_vector(user, top_ten_users, weighted)
    return get_precision_at_ten(ranking_vector)

if __name__ == '__main__':
    pass