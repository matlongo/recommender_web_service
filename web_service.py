# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:07:48 2017

@author: mathias
"""

#!/usr/bin/env python
import web
from recommender import Recommender
import json

urls = (
    '/data/recommendations', 'get_recommendations',
    '/data/add', 'add_data',
    '/data/songs', 'list_songs',
    '/data/users', 'list_users'
)

recommender = Recommender('to_train.csv')
app = web.application(urls, globals())

class get_recommendations:
    """
    This class defines the functionality to get the recommendations for a given
    user. It first gets the user_id given in the querystring with the following
    format: [ip]:[port]/data/recommendations?user_id=[user_id]. Once the
    querystring is parsed, the user_id is obtained and the recommender object
    is invoked.
    It finally returns the recommendations in a JSON response.
    """
    def GET(self):
        input_data = web.input(user_id=None)
        user_id = input_data['user_id']
        #if user_id is None:
        #    return web.internalerror("To get a recommendation, a user_id should be given in the query-string.")
        user_id = str(user_id)
        recs = recommender.get_recommendations(user_id, 4)
        response = {'recommendations': list(recs)}
        
        web.header('Content-Type', 'application/json')
        return json.dumps(response)

class add_data:
    """
    This class implements the POST function to add a new user-song interaction.
    Whenever a user plays a song it is added to the service so that the 
    recommendations are kept up to date. The post body should contain two key-
    value fields: user_id=[user_id] and song_id=[song_id].
    Once all the data is obtained and parsed, this function calls the recommender's 
    add_data function, and if everything is ok it returns an OK JSON.
    """
    def POST(self):
        dic = web.input(user_id=None, song_id=None)
        user_id = dic['user_id']
        song_id = dic['song_id']
        #if user_id is None or song_id is None:
        #    return web.internalerror("There was an error parsing the query-string. A valid user_id and song_id should be given in the query-string.")
        
        user_id = str(user_id)
        song_id = str(song_id)
        recommender.add_data(user_id, song_id)
        response = {'user_id': user_id, 'song_id': song_id, 'response': 'interaction successfully added'}
        
        web.header('Content-Type', 'application/json')
        return json.dumps(response)
        
class list_songs:
    """
    It returns the whole list of songs already loaded in the system.
    """
    def GET(self):
        songs = recommender.get_songs()
        response = {'songs': songs}
        
        web.header('Content-Type', 'application/json')
        return json.dumps(response)

class list_users:
    """
    It returns the whole list of users already loaded in the system.
    """
    def GET(self):
        users = recommender.get_users()
        response = {'users': users}
        
        web.header('Content-Type', 'application/json')
        return json.dumps(response)

if __name__ == "__main__":
    app.run()
