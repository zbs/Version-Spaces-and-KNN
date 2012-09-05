'''
Created on Sep 3, 2012

@author: zach
'''
class User():
    def __init__(self, user_line=None, user_id=None, user_songs=None):
        if user_id and user_songs:
            self.id, self.songs = user_id, user_songs
        else:    
            self.id, songs = user_line.split(' - ') 
            self.id = int(self.id)
            def f(x):
                y = x.split(':')
                y[1] = int(y[1])
                return tuple(y)
            self.songs = dict(map(f, songs.split(' ')))
    
    def get_similarity_funct(self, similarity_metric):
        return lambda other_user: similarity_metric(self, other_user)
    
    def __str__(self):
        return 'User ID = %s; Songs = %s'%(self.id, str(self.songs))
    
    def __repr__(self):
        return 'User ID = %s; Songs = %s'%(self.id, str(self.songs))