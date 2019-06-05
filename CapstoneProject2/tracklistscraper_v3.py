#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 00:43:05 2019

@author: Jin
"""
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from bs4 import BeautifulSoup
#from splinter import Browser
#from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import unicodedata
from urllib.request import urlopen
#import urllib2
#from tracklist_browser import TL_webpages_names
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from spotifyxx_v4 import get_audio_features
import re

executable_path = {"executable_path":"/users/jin1/Desktop/Springboard/Projects/chromedriver"}

TL_songFeatures = []
TL_Data = []

#Creating dictionary which will record each song's metadata
song_dict = {
    "TL_Name": "",
    "TL_URL": "",
    "TL_SC_Link": "None",
    "TL_Youtube_Link": "None", 
    "TL_Date": "",
    "TL_Views": "",
    "TL_Likes": "",
    "TL_Number_IDed": "",
    "TL_Genres": "",
    "TL_Sources": "",
    "TL_Avg_Spotify_Danceability": 0,
    "TL_Avg_Spotify_Energy": 0,
    "TL_Avg_Spotify_Tempo": 0,
    "TL_Avg_Spotify_Valence": 0,
    "TL_SongName": "",
    "TL_SongArtist": "",
    "TL_SongRemixFlag": False,
    "TL_PositionSeconds": "",
}


column_names = song_dict.keys()

#Creating dictionary which will record Spotify data for each identified song in each set/mix
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

#Function called get_all_data to get each tracklist's data:
def get_all_data(test_soup):
    return get_number_of_tracks(test_soup)

#Helper Function called get_number_of_tracks that gets number of songs in tl and intialized list of dictionaries
def get_number_of_tracks(test_soup):
    #Initializing list to count number of songs and list of dictionaries
    number_of_songs_list = []
    TL_Songs = []
    number_of_songs = 0
    TL_Data = []
    
    
    """
    #Filling in list
    for tag in test_soup.find_all('table', class_="default full tl hover"):
        #Getting position in mix in seconds
        for tag in test_soup.find_all('input', id = True, type = "hidden", value=True):
            number_of_songs_list.append(tag)
            #print(number_of_songs_list[-1])
        number_of_songs = int(''.join([x for x in str(number_of_songs_list[-1]) if x.isdigit()]))
        #number_of_songs = int(list(filter(str.isdigit, str(number_of_songs_list[-1])))) + 1
    """
    
    #Tracks
    track_div_container = []
    for track in test_soup.find_all('div', itemprop="tracks"):
        track_div_container.append(track)
    
    
    #Creating list of dictionaries, with each element in the list being a song
    for i in range(len(track_div_container)):
        #Converting element of list to dictionary defined above
        i = song_dict.copy()
        TL_Songs.append(i)
        
    
    #get_track_time(test_soup, TL_Songs)
    Updated_TL_Songs = get_track_artist_and_song(test_soup, TL_Songs)
    Updated_TL_Songs = get_tracklist_metadata(test_soup, Updated_TL_Songs)
    

    #for song in TL_Songs:
    #    TL_Data.append(song)
    #print(TL_Songs)
    
    return Updated_TL_Songs



###Scraping each track's metadata  
#Helper Function called get_track_time to get track's position in mix in seconds
"""
def get_track_time(test_soup, tracklist_list):
    #Counters
    song_counter = 1
    
    
    for tag in test_soup.find_all('input', id = True, type = "hidden", value=True):
        if "seconds" in tag.get('id'):
            position_in_mix = tag.get('value')
            #print("Song " + str(song_counter) + ": " + position_in_mix)
            tracklist_list[song_counter - 1]["TL_PositionSeconds"] = position_in_mix
            song_counter = song_counter + 1
    
    
            
            #Gets position in mix in mm:ss format
            #for tag in test_soup.find_all('div', class_='cueValueField action'):
            #print(tag)
                 
    #Resetting song counter
    song_counter = 1
"""


#Helper Function called get_track_artist_and_song to get track's artist and song name info
def get_track_artist_and_song(test_soup, tracklist_list):
    
    #Creating Counters and Flags
    song_remix_flag = False
    song_remix_name = ""
    song_counter = 1
    

    #Creating container containing all metadata for each track to iterate over
    #for tag in test_soup.find_all('table', class_="default full tl hover"):    
    #Getting each tracks details
    track_div_container = []
    for track in test_soup.find_all('div', itemprop="tracks"):
        track_div_container.append(track)
    
    #track_div_container = test_soup.find_all('div', itemprop="tracks")

    #Iterating over container of tracks to get metadata
    for container in track_div_container:
        for tag in container.find_all('meta'):
            #flagging if track is a remix
            if tag.get('itemprop') == 'name' and "Remix" in tag.get('content'):
                #if "Remix" in tag.get('content'):
                song_remix_flag = True
                song_remix_name = tag.get('content')
                tracklist_list[song_counter - 1]["TL_SongRemixFlag"] = song_remix_flag

            #getting details for each track while accounting for remix flag
            if song_remix_flag == True and tag.get('itemprop') == 'name':
                #if tag.get('itemprop') == 'name':
                #song_artist_name = str(tag.get('content')).rsplit('(', 1)[1].rsplit('Remix',1)[0]
                song_artist_name = tag.get('content').rsplit('(', 1)[1].rsplit('Remix',1)[0]
                song_name = song_remix_name
                tracklist_list[song_counter - 1]["TL_SongArtist"] = song_artist_name
                tracklist_list[song_counter - 1]["TL_SongName"] = song_name
                
            else:
                if tag.get('itemprop') == 'byArtist':
                    song_artist_name = tag.get('content')
                    tracklist_list[song_counter - 1]["TL_SongArtist"] = song_artist_name
                if tag.get('itemprop') == 'name':
                    song_name = tag.get('content')
                    tracklist_list[song_counter - 1]["TL_SongName"] = song_name
                
        
        song_remix_flag = False
        song_counter = song_counter + 1

    #Resetting song counter
    song_counter = 1
    
    return tracklist_list

#Helper Function called get_tracklist_metadata that gets Tracklist's metadata
def get_tracklist_metadata(test_soup, track_list):
    
    #Creating Counters and Flags
    TL_visits =  0
    TL_likes = 0
    TL_date = ""
    TL_genres = ""
    TL_name = ""
    TL_sources = ""
    
    #Getting Tracklist likes and views
    for tag in test_soup.find_all('meta', itemprop='interactionCount'):
        if "Visits" in tag.get('content'):
            #TL_visits = int(filter(str.isdigit, str(tag.get('content'))))
            TL_visits = int(''.join([x for x in str(tag.get('content')) if x.isdigit()]))
            

        if "Likes" in tag.get('content'):
            #TL_likes = int(filter(str.isdigit, str(tag.get('content'))))
            TL_likes = int(''.join([x for x in str(tag.get('content')) if x.isdigit()]))
            
        
    #Getting Tracklist date
    for tag in test_soup.find_all('meta', itemprop='datePublished'):
        TL_date = str(tag.get('content'))[0:10]
        

    #Getting Tracklist genre
    for tag in test_soup.find_all('td', id='tl_music_styles'):
        #looks like contents is a list of styles, so concat into 1 string
        styles = ""
        for style in tag.contents:
            styles = styles + style
        TL_genres = styles
        

    #Getting tracklist name
    for tag in test_soup.find_all('meta', itemprop='headline'):
        TL_name = tag.get('content')
        

    #This is code to find tracklist event/source
    for tag in test_soup.find_all('tr', class_='tlGroupItem'):
        TL_sources = tag.contents[1].string 
    
    #Getting Spotify IDs of each identified track in set/mix
    TL_Spotify_IDs = []
    for tag in test_soup.find_all('iframe', src=re.compile("open.spotify.com/embed/track/")):
        Spotify_ID = tag.get('src').rsplit('/', 1)[1]
        TL_Spotify_IDs.append(Spotify_ID)
    
    #Accessing Spotify's web API to get audio features of identified tracks in set/mix
    TL_songFeatures = get_audio_features(TL_Spotify_IDs)
        
    #Creating a dataframe with scraped tracklist spotify IDs
    TL_songFeatures_dicts = []
    for i in range(len(TL_Spotify_IDs)):
        i = song_features.copy()
        TL_songFeatures_dicts.append(i)

    
    if(len(TL_songFeatures_dicts) != 0):
        counter = 0
        for item in TL_songFeatures:
            TL_songFeatures_dicts[counter]["key"] = item["key"]
            TL_songFeatures_dicts[counter]["mode"] = item["mode"]
            TL_songFeatures_dicts[counter]["time_signature"] = item["time_signature"]
            TL_songFeatures_dicts[counter]["acousticness"] = item["acousticness"]
            TL_songFeatures_dicts[counter]["danceability"] = item["danceability"]
            TL_songFeatures_dicts[counter]["energy"] = item["energy"]
            TL_songFeatures_dicts[counter]["loudness"] = item["loudness"]
            TL_songFeatures_dicts[counter]["tempo"] = item["tempo"]
            TL_songFeatures_dicts[counter]["id"] = item["id"]
            TL_songFeatures_dicts[counter]["uri"] = item["uri"]
            TL_songFeatures_dicts[counter]["instrumentalness"] = item["instrumentalness"]
            TL_songFeatures_dicts[counter]["valence"] = item["valence"]
            counter = counter + 1

        TL_songFeatures_DF = pd.DataFrame(TL_songFeatures_dicts)
        #Resetting list of dictionaries
        TL_songFeatures_dicts = []
        
        for track in track_list:
            track["TL_Avg_Spotify_Danceability"] = TL_songFeatures_DF["danceability"].mean()
            track["TL_Avg_Spotify_Energy"] = TL_songFeatures_DF["energy"].mean()
            track["TL_Avg_Spotify_Tempo"] = TL_songFeatures_DF["tempo"].mean()
            track["TL_Avg_Spotify_Valence"] = TL_songFeatures_DF["valence"].mean()
    
    """
    #Getting number of ID'ed tracks
    for tag in test_soup.find_all('tr', class_=' '):
        for child in tag.descendants:
            if child != " ":
                TL_IDed = child
                return TL_IDed
            
    #If all IDed, then first character is blank
    if TL_IDed[0] == " ":
        TL_IDed = "All IDed"
        return TL_IDed
    """
    
    #Recording all tracklist metadata
    for track in track_list:
        track["TL_Views"] = TL_visits
        track["TL_Likes"] = TL_likes
        track["TL_Date"] = TL_date
        track["TL_Genres"] = TL_genres
        track["TL_Name"] = TL_name
        track["TL_Sources"] = TL_sources
        #track["TL_Avg_Spotify_Danceability"] = TL_songFeatures_DF["danceability"].mean()
        #track["TL_Avg_Spotify_Energy"] = TL_songFeatures_DF["energy"].mean()
        #track["TL_Avg_Spotify_Tempo"] = TL_songFeatures_DF["tempo"].mean()
        #track["TL_Avg_Spotify_Valence"] = TL_songFeatures_DF["valence"].mean()
        #track["TL_URL"] = TL_webpages_names[TL_counter]
        #track["TL_Number_IDed"] = TL_IDed

    return track_list


#Test Code
"""
test_soup = BeautifulSoup(TL_final_htmls[0])

track_div_container = []
for track in test_soup.find_all('div', itemprop="tracks"):
    track_div_container.append(track)

track_div_container[23]
"""


"""
#test_page = "https://www.1001tracklists.com/tracklist/zuwch91/ekali-kineticfield-edc-china-guangdong-2018-11-24.html"
#test_page = "https://www.1001tracklists.com/tracklist/2wd8ru3k/ekali-orlando-amphitheater-united-states-2019-02-02.html"
#test_page = "https://www.1001tracklists.com/tracklist/2l44qn0t/ekali-awakening-radio-004-2018-11-06.html"
test_page = 'https://www.1001tracklists.com/tracklist/j0nxrgt/nghtmre-slander-mainstage-ultra-music-festival-miami-miami-music-week-united-states-2019-03-30.html'
#test_page = 'test.html'
page = urlopen(test_page)
#page = urllib2.urlopen(test_page)
#page = 'test.html'
test_soup = BeautifulSoup(page)

for tag in test_soup.find_all('a', href = True):
    print(tag.get('href'))





TL_DF = pd.DataFrame()
#get_all_data(test_soup)
column_names = song_dict.keys()
#TL_DF = pd.DataFrame(TL_Data, columns = column_names)
TL_DF= pd.DataFrame.from_records(TL_Data, columns = column_names)

print(TL_DF.head())


writer = pd.ExcelWriter(r'/Users/jin1/Desktop/1001tracklistdata.xlsx', engine='xlsxwriter')
#writer = pd.ExcelWriter(r'/Users/a0709761/Desktop/1001tracklistdata.xlsx', engine='xlsxwriter')
TL_DF.to_excel(writer, sheet_name = 'Sheet_name_1')
writer.save()
writer.close()


#Notes
#track_div_container[9].contents[5].contents[1].contents[1].contents[1].contents[1].get('class')
track_div_container[9].contents[5].find_all('span', title = True)[1]

#Flagging if remix or mashup
track_div_container[9].find_all('span', class_='trackFormat mashupTrack')[0]
track_div_container[9].find_all('span', class_='remixValue blueTxt')


for tag in track_div_container[9].find_all('meta'):
    print(tag.get('itemprop'))
    print(tag.get('content'))


for container in track_div_container:
    for tag in container.find_all('meta'):
        #print(tag.get('itemprop'))
        #print(tag.get('content'))
        print(tag)


for container in track_div_container:
    for tag in container.find_all('span', title = True):
        print(tag.get('itemprop'))
        print(tag.get('content'))
        print(tag)
#print(container.find_all('meta').get('content'))

#soup = BeautifulSoup(open("C:\\example.html"), "html.parser")

#for city in soup.find_all('span', {'class' : 'city-sh'}):
#    print(city)


for tag in test_soup.find_all('a', href = True):
    print(tag.get('href'))
"""


   





