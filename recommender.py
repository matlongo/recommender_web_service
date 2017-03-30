# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:48:01 2017

@author: mathias
"""

import graphlab as gl

class Recommender:
    def __init__(self, path_to_data):
        self.__path_to_data = path_to_data
        self.__new_data = None
        self.create_model()
        self.__update_threshold = 50
        print "Recommender initialized"
    
    def get_recommendations(self, user, k=4):
        """
        This function returns a k set of recommendations for a given user. If
        the user is not the system yet, it returns the most popular songs.
        - user: user id to which we are going to look for recommendations.
        - k: number of recommendations returned.
        """
        print "Recommendations for user", user
        
        if self.__new_data is not None:
            return self.__model__ .recommend(users=[user], k=k, verbose=True,
                                      new_observation_data = self.__new_data)['song_id']

        return self.__model__ .recommend(users=[user], k=k, verbose=True)['song_id']
    
    def add_data(self, user_id, song_id):
        """
        Given a user and a song interaction, this function adds the new interaction
        to the new data. If the number of new rows gets a previously specified
        threshold it updates the model with the new data.
        """
        assert user_id is not None, "The user_id is null"
        assert song_id is not None, "The song_id is null"
        #print user_id, song_id, self.__new_data
        if self.__new_data is None:
            self.__new_data = gl.SFrame({'user_id':[user_id], 'song_id':[song_id]})
        else:
            self.__new_data = gl.SFrame({'user_id':[user_id], 
                                     'song_id':[song_id]}).append(self.__new_data)
        if (self.__new_data.shape[0] > self.__update_threshold):
            print "It's gonna be updated"
            self.update()
        return 0
        
    def update(self):
        """
        When the number of data added gets the threshold the model is updated.
        Once everything is updated, the new_data is deleted and set to None 
        again.
        """
        self.create_model()
        del self.__new_data
        self.__new_data = None
        return 0
        
    def create_model(self):
        """
        This function creates the item-based GraphLab model. In order to do so
        it first reads the history data stored, it then appends the new_data
        to the read data and creates the model. To back-up it also saves the 
        model, and overwrites the data stored with the new set of data. Finally,
        it deletes the data that is useless for the execution.
        """
        self.__data = gl.SFrame.read_csv(self.__path_to_data, delimiter=',', 
                           verbose=False, header=True)
        #self.__data = self.__data.rename({'X1': 'user_id', 'X2': 'song_id'})
        if self.__new_data is not None:
            self.__data = self.__new_data.append(self.__data)
        self.__model__ = gl.recommender.item_similarity_recommender.create(self.__data, 
                                item_id='song_id', user_id='user_id', 
                                similarity_type='jaccard', verbose=False)
        self.__model__.save('jaccard_recommender')
        self.__data[['user_id', 'song_id']].export_csv(self.__path_to_data, header=True)
        self.__users = self.__data['user_id'].unique()
        del self.__data
        print "Recommender created"
        
        return 0
    
    def get_songs(self):
        """
        Returns the list of all the songs loaded in the recommender.
        """
        songs = self.__model__.recommend(users=['a'], k=self.__model__.get('num_items'))
        return list(songs['song_id'])
    
    def get_users(self):
        """
        Returns the list of all the users loaded in the recommender.
        """
        return list(self.__users)
        
        
        
        