'''
Created on Sep 4, 2012

@author: zach
'''
from SongRecommendation.Main import *
import SongRecommendation.User
import unittest


class Test(unittest.TestCase):

    
    def setUp(self):
        self.user1_songs = dict([(2,3), (3,4), (5,1)])
        self.user2_songs = dict([(1,2), (2,2), (5,5), (6,2)]) 
        


    def tearDown(self):
        pass


    def testName(self):
        self.assertEqual(euclidean_distance(self.user1_songs, self.user2_songs), 0.15617376188860607, 'euclidean_distance fails')
        self.assertEqual(dot_product(self.user1_songs, self.user2_songs), 11, 'dot product fails')
        self.assertAlmostEqual(cos_distance(self.user1_songs, self.user2_songs), 0.35465423412053854, places=5)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()