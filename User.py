import spotipy
import json
import flask
from flask import request
import pymongo
from pymongo import errors

app = flask.Flask(__name__)

@app.route("/python")
def index():

    access_token = request.args.get('token')
    print(access_token)

    scope = 'user-top-read'
    token = access_token

    print(token)
    if token:
        sp = spotipy.Spotify(token)
        sp.trace = False
        ranges = ['short_term', 'medium_term', 'long_term']
        top_artists = sp.current_user_top_artists(10, 0, ranges[1])
        top_tracks = sp.current_user_top_tracks(10, 0, ranges[1])
        user_id = sp.current_user()["id"]
    else:
        print("Can't get token for")
        sp = "No Results"
        top_artists = "No Results"
        top_tracks = "No Results"
        results = "No Results"

    user_id = sp.current_user()["id"]

    json_string_android = '{"top_artists":' + json.dumps(top_artists, indent=4) + ',"top_tracks":' + json.dumps(top_tracks,
                                                                                                        indent=4) + "}"
    json_string_mongo = '{"spotifyId":' + str(user_id) + "," + '"top_artists":' + json.dumps(
        top_artists, indent=4) + ',"top_tracks":' + json.dumps(top_tracks, indent=4) + "}"

    json_data = json.loads(json_string_mongo)

    my_client = pymongo.MongoClient()

    try:
        my_client = pymongo.MongoClient("mongodb+srv://nschafer99:FusionNSmongo@cluster0-3dhag.mongodb.net/admin?retryWrites=true&w=majority",
                                        connectTimeoutMS=10000, serverSelectionTimeoutMS=10000)
        my_db = my_client["fusion_db"]
        my_col = my_db["customers"]
        if my_col.count_documents({"spotifyId": int(user_id)}) > 0:
            print("Already exists")
        else:
            my_col.insert_one(json_data)
    except pymongo.errors.ConnectionFailure as e:
        print("Error occurred", e)

    my_client.close()

    # Return json_string to the Android application
    return json_string_android


if __name__ == '__main__':
    app.run()
