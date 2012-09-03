'''
Created on Sep 3, 2012

@author: zach
'''
class User():
    def __init__(self, user_line):
        self.user, songs = user_line.split(' - ') 
        def f(x):
            y = x.split(':')
            y[1] = int(y[1])
            return tuple(y)
        self.songs = dict(map(f, songs.split(' ')))

    def get_cmp_funct(self, similarity_metric):
        def similarity_cmp(user1, user2):
            return similarity_metric(self.songs, user2.songs) - \
                    similarity_metric(self.songs, user1.songs)
        return similarity_cmp