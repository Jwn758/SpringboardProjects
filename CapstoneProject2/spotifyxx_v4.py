#Jin

import os
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
import spotipy
import webbrowser
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import numpy as np
#from openpyxl import Workbook
#from json.decoder import JSONDecodeError
#import simplejson as json


#from main import Master_DF


scope = 'user-follow-read user-read-private user-read-playback-state user-modify-playback-state user-library-read user-top-read'

"""
# Get the username from terminal
#username = sys.argv[1]
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
"""

#username = sys.argv[1]
username = '1218216809'

#nanditas
#username = '1297035328'

#davids
#username = '12144292721'
#angels
#username = '22si25h5wgt4bujzwb5fay77a'
#rays
#wills
#username = 'williamchan2017?'

#https://open.spotify.com/user/williamchan2017?si=xhpSeWxKQM2Itx2SOYPCJg

#rchen5-us?si=Mh13EELwREKTr99-XXdbrQ

client_id = 'cff938817e47450aa485a63bcb809868'
client_secret = '3ca8450ef3b842779970e8281f613cbb'
redirect_uri = 'http://google.com/'
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


"""
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
"""


# Erase cache and prompt for user permission
"""
try:
    token = util.prompt_for_user_token(username, scope) # add scope
#except (AttributeError, JSONDecodeError):
except:
    os.remove(".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope
"""


# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)


#code to get current user's current song that is being played and artist
"""
# Get current device
devices = spotifyObject.devices()
#deviceID = devices["devices"][0]["id"]
#deviceID = devices["devices"][0]["id"]

# Current track information
track = spotifyObject.current_user_playing_track()
artist = track["item"]["artists"][0]["name"]
track = track["item"]["name"]

if artist != "":
    print("Currently playing " + artist + " - " + track)
"""


# User information
user = spotifyObject.current_user()
displayName = user["display_name"]
followers = user["followers"]["total"]


top_songs = []


#Extract User Data
#topArtists = spotifyObject.current_user_top_tracks()
#topSongs = spotifyObject.current_user_saved_tracks()
#print("Top Saved Tracks:")
#print()
results = spotifyObject.current_user_saved_tracks()

saved_song = {
        "song_name": "",
        "song_artist": "",
        "song_id": "",
}

tids = []
tnames = []
tartists = []

saved_songs = []
for i in range(len(results["items"])):
    i = saved_song.copy()
    saved_songs.append(i)

for item in results["items"]:
    track = item["track"]
    print(track["name"] + ' - ' + track["artists"][0]["name"])

counter = 0
for item in results["items"]:
    track = item["track"]
    saved_songs[counter]["song_name"] = track["name"]
    saved_songs[counter]["song_artist"] = track["artists"][0]["name"]
    saved_songs[counter]["song_id"] = track["id"]
    tids.append(track["id"])
    tnames.append(track["name"])
    tartists.append(track["artists"][0]["name"])
    counter = counter + 1

#print("Top Tracks")
#print()
results = spotifyObject.current_user_top_tracks(limit = 50)
for i, item, in enumerate(results["items"]):
    print(i, item["name"], item['artists'][0]['name'])

for i in range(len(results["items"])):
    i = saved_song.copy()
    top_songs.append(i)    

counter = 0
for item in results["items"]:
    top_songs[counter]["song_name"] = item["name"]
    top_songs[counter]["song_artist"] = item['artists'][0]['name']
    top_songs[counter]["song_id"] = item['id']
    tids.append(item['id'])
    tnames.append(item["name"])
    tartists.append(item['artists'][0]['name'])
    counter = counter + 1


#print("Top Artists")
#print()
topArtists = spotifyObject.current_user_followed_artists()

artist_dict = {
        "artist_name": "",
        "artist_genre": "",
        "artist_popularity": 0,
        "artist_followers": 0,
}

topArtists_dicts = []
for i in range(len(topArtists['artists']['items'])):
    i = artist_dict.copy()
    topArtists_dicts.append(i)
    
counter = 0
for item in topArtists['artists']['items']:
    print(item['name'])
    print(item['genres'])
    print(item['popularity'])
    print(item['followers']['total'])
    topArtists_dicts[counter]["artist_name"] = item['name']
    topArtists_dicts[counter]["artist_genre"] = item['genres']
    topArtists_dicts[counter]["artist_popularity"] = item['popularity']
    topArtists_dicts[counter]["artist_followers"] = item['followers']["total"]
    tartists.append(item['name'])
    counter = counter + 1


#print("Song Features")
print()
def get_audio_features(list_of_ids):
    token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    spotifyObject = spotipy.Spotify(auth=token)
    return spotifyObject.audio_features(list_of_ids)


songFeatures = get_audio_features(tids)
#spotifyObject.trace = True


#print(songFeatures)

song_features = {
        "key": 0,
        "mode": 0,
        "time_signature": 0,
        "acousticness": 0,
        "danceability": 0,
        "energy": 0,
        "loudness": 0,
        "tempo": 0,
        "id": "",
        "uri": "",
        "instrumentalness": 0,
        "valence": 0,
        "name": "",
}

songFeatures_dicts = []
for i in range(len(tids)):
    i = song_features.copy()
    songFeatures_dicts.append(i)

counter = 0
for item in songFeatures:
    songFeatures_dicts[counter]["name"] = tnames[counter]
    songFeatures_dicts[counter]["key"] = item["key"]
    songFeatures_dicts[counter]["mode"] = item["mode"]
    songFeatures_dicts[counter]["time_signature"] = item["time_signature"]
    songFeatures_dicts[counter]["acousticness"] = item["acousticness"]
    songFeatures_dicts[counter]["danceability"] = item["danceability"]
    songFeatures_dicts[counter]["energy"] = item["energy"]
    songFeatures_dicts[counter]["loudness"] = item["loudness"]
    songFeatures_dicts[counter]["tempo"] = item["tempo"]
    songFeatures_dicts[counter]["id"] = item["id"]
    songFeatures_dicts[counter]["uri"] = item["uri"]
    songFeatures_dicts[counter]["instrumentalness"] = item["instrumentalness"]
    songFeatures_dicts[counter]["valence"] = item["valence"]
    #songFeatures_dicts[counter]["key"] = item["key"]
    counter = counter + 1





#print(topArtists_dicts)
#print(top_songs)
#print(saved_songs)


#Used spotify user's top artists, top songs, and saved songs to make unique list of songs and artist names
unique_artists = []
unique_artists = list(set(tartists))
unique_songs = []
unique_songs = list(set(tnames))


topArtists_DF = pd.DataFrame(topArtists_dicts)
top_songs_DF = pd.DataFrame(top_songs)
saved_songs_DF = pd.DataFrame(saved_songs)
songFeatures_DF = pd.DataFrame(songFeatures_dicts)

songFeatures_DF["danceability"].mean()
songFeatures_DF["energy"].mean()
songFeatures_DF["tempo"].mean()
songFeatures_DF["danceability"].mean()


artist_regex_pattern = '|'.join(unique_artists)
song_regex_pattern = '|'.join(unique_songs)




topArtists_DF["EDM_Artist"] = topArtists_DF["artist_genre"].map(lambda x: "edm" in x)

edmArtists_DF = topArtists_DF.loc[(topArtists_DF["EDM_Artist"] == True)]


#Creating unique list of edm artists to search with selenium on 1001tracklists.com
unique_edmArtists = []
unique_edmArtists = list(edmArtists_DF["artist_name"])




#print(topArtists_DF.head())
#print(top_songs_DF.head())
#print(saved_songs_DF.head())
#print(songFeatures_DF.describe())

tids

"""
#Writing to Excel file for easier EDA
with pd.ExcelWriter('jinsspotifydata3.xlsx') as writer:
    topArtists_DF.to_excel(writer, sheet_name='Top_Artists')
    top_songs_DF.to_excel(writer, sheet_name='Top_Songs')
    saved_songs_DF.to_excel(writer, sheet_name='Saved_Songs')
    songFeatures_DF.to_excel(writer, sheet_name = 'Song_Features')
    writer.save()
"""

#print(json.dumps(topArtists, sort_keys=True, indent=4))

# Loop
"""
while True:
    # Main Menu
    print()
    print(">>> Welcome to Spotipy " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    #print("Your Top Artists are:")
    ###print(topArtists)
    
    #print("Your Top Songs are:")
    ###print(topSongs)
    
    
    choice = input("Your choice: ")

    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        #webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']


        # Album and track details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()
        
        
        
        
        

    if choice == "1":
        break

    # print(json.dumps(trackResults, sort_keys=True, indent=4))
"""