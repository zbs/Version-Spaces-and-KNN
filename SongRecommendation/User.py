'''
Created on Sep 3, 2012

@author: zach
'''
class User():
    def __init__(self, user_line):
        self.id, songs = user_line.split(' - ') 
        self.id = int(self.id)
        def f(x):
            y = x.split(':')
            y[1] = int(y[1])
            return tuple(y)
        self.songs = dict(map(f, songs.split(' ')))
    
    def get_similarity_funct(self, similarity_metric):
        return lambda other_user: similarity_metric(self.songs, other_user.songs)
    
    def get_cmp_funct(self, similarity_metric):
        def similarity_cmp(user1, user2):
            return similarity_metric(self.songs, user2.songs) - \
                    similarity_metric(self.songs, user1.songs)
        return similarity_cmp
    
    def __str__(self):
        return 'User ID = %s; Songs = %s'%(self.id, str(self.songs))
    
    def __repr__(self):
        return 'User ID = %s; Songs = %s'%(self.id, str(self.songs))