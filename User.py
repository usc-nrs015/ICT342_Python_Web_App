import spotipy
import spotipy.util as util

import flask
from flask import request
app = flask.Flask(__name__)

@app.route("/python")
def index():
    ''''
    access_token = request.args.get('token')
    print(access_token)

    scope = 'user-top-read'
    username = 'nscha14'
    token = access_token

    '''
    #token = util.prompt_for_user_token(username, scope,
                  #                     client_id='0281ed7b2a594e66a3b4a6c545b09000',
                  #                     client_secret='99ba40fe5a2b43828c24da1da1d755b1',
                   #                    redirect_uri='http://localhost/')
    '''

    print(token)
    if token:
        sp = spotipy.Spotify(token)  # Goal is to get token from mobile app that is stored.
        sp.trace = False
        ranges = ['short_term', 'medium_term', 'long_term']
        results = sp.current_user_top_artists(1, 0, ranges[1])
        results2 = sp.current_user_top_tracks(1, 0, ranges[1])
        print(results)
        # for i, item in enumerate(results['items']):
        # print( i, item['name'])
    else:
        print("Can't get token for", username)
    
    return "Hello Heruko " + access_token
    '''
    return "hello"
