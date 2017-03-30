# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:38:03 2017

@author: mathias
"""
#%%
import requests
import numpy as np
import pandas as pd
import thread
import time

#%%
all_users = pd.read_csv('all_users.csv', names=['user_id'])
N_u = all_users.shape[0]
to_add = pd.read_csv('to_add.csv', names=['user_id', 'song_id'])

#%%
def get_recommendations(user=None, n=1, verbose=True, sleeps=False):
    """
    This function asks the web service for n-recommendations. If user is None,
    for each recommendation the function picks a random user from the whole 
    database.
    """
    for i in range(n):
        # We pick a random user
        pos = np.random.randint(0, N_u)
        user_id = all_users['user_id'].iloc[pos]
        # We define the url and the query
        url = 'http://localhost:8080/data/recommendations?user_id={0}'.format(user_id)
        res = requests.get(url)
        
        # We ensure that everything is ok
        try:
            recs = pd.read_json(res.text)
        except:
            raise Exception("The response is malformed.")
        assert recs.shape[0] == 4, "The number of recommendations is incorrect."
        assert sum(map(lambda r: r[0]=='S', recs['recommendations'])) == 4, "The recommendations given are incorrect"
        if verbose:        
            print "Recommendations: ", recs['recommendations'].tolist()
        if sleeps:
            # We put to sleep the thread for a random time between [0:3] secs
            time.sleep(np.random.random()*3)
    
    print "Recommendations Finished"


def add_data(from_=0, n=1, verbose=True, sleeps=False):
    """
    This function adds a given a number of user-song interactions.
    """
    for i in range(from_, n+from_):
        # We first get the data to be added
        user_id = to_add.iloc[i]['user_id']
        song_id = to_add.iloc[i]['song_id']
        data = {'user_id':user_id, 'song_id':song_id}
        # We define the url
        url = 'http://localhost:8080/data/add'
        # Finally we send the post query
        res = requests.post(url, data=data)
        
        # We check everything is ok
        try:
            res_s = pd.read_json(res.text, typ='series')
        except:
            raise Exception("The response is malformed.")
        assert res_s['response'] == "interaction successfully added", "The interaction was not successfully added."
        assert res_s['song_id'] == song_id, "The song_id is not the same that was added."
        assert res_s['user_id'] == user_id, "The user_id is not the same that was added."
        
        if verbose:
            print "Adding: ", res.text
        if sleeps:
            # We put to sleep the thread for a second
            time.sleep(1)
            
    print "Addition Finished"

#%%
thread.start_new_thread(get_recommendations, (None, 3, True, True))
thread.start_new_thread(add_data, (0, 3, True, True))


