#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 20:04:34 2019

@author: Jin
"""
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd

#Importing from other files
from spotifyxx_v4 import *
from tracklist_browser import TL_final_htmls
from tracklistscraper_v3 import *

#Initializing Master DF
Master_DF = pd.DataFrame()

#Import TL_final_htmls from tracklistbrowser.py and run scraper
for html in TL_final_htmls[0:6]:
    test_soup = BeautifulSoup(html)
    Next_Array = get_all_data(test_soup)
    TL_DF = pd.DataFrame.from_records(Next_Array, columns = column_names)
    Master_DF = pd.concat([TL_DF, Master_DF])

    
#Output master tracklist dataframe to excel for easier exploration
writer = pd.ExcelWriter(r'/Users/jin1/Desktop/masterdata0604.xlsx', engine='xlsxwriter')
Master_DF.to_excel(writer, sheet_name = 'Sheet_name_1')
writer.save()
writer.close()



test_soup = BeautifulSoup(TL_final_htmls[0])
get_all_data(test_soup)



"""
#Test Code when testing locally
test_page = 'test.html'
page = urlopen(test_page)
#page = urllib2.urlopen(test_page)
#page = 'test.html'
test_soup = BeautifulSoup(page)

#Test Code when testing locally
test_page = 'test.html'
page = urlopen(test_page)
test_soup = BeautifulSoup(page)
get_all_data(test_soup)
"""


"""
#Recommendation Algorithm
    
#Converting spotify user's unique artists and songs into regex pattern
artist_regex_pattern = '|'.join(unique_artists)
song_regex_pattern = '|'.join(unique_songs)



#Creating a new column in dataframe if artist match is found in tracklist
Master_DF["New_Col_Artist_Flag"] = Master_DF["TL_SongArtist"].str.contains(artist_regex_pattern).fillna('')

#Creating a new collumn in dataframe if song match is found in tracklist
Master_DF["New_Col_Song_Flag"] = Master_DF["TL_SongArtist"].str.contains(song_regex_pattern).fillna('')

Master_DF.groupby("TL_Name")["New_Col_Artist_Flag"].value_counts()

#master_data = pd.read_hdf('/Users/jin1/Desktop/1001tracklistdata.xlsx')


writer = pd.ExcelWriter(r'/Users/jin1/Desktop/jins1001tracklistdata0602.xlsx', engine='xlsxwriter')
TL_DF.to_excel(writer, sheet_name = 'Sheet_name_1')
writer.save()
writer.close()
"""




###Test Code
"""
#Outputting master DF to excel for easier EDA
writer = pd.ExcelWriter(r'/Users/jin1/Desktop/jins1001tracklistdata.xlsx', engine='xlsxwriter')
Master_DF.to_excel(writer, sheet_name = 'Sheet_name_1')
writer.save()
writer.close()
"""

"""
#Going through each imported URL that contains the tracklist of each artist user listens to
for tracklist in TL_webpages_names[0:3]:
    test_page = tracklist
    page = urlopen(test_page)
    test_soup = BeautifulSoup(page)
    get_all_data(test_soup)
    TL_DF = pd.DataFrame.from_records(TL_Data, columns = column_names)
    #Master_DF = pd.concat([Master_DF, TL_DF], ignore_index = True)
"""


"""
test_list = []
test_list = ['https://www.1001tracklists.com/tracklist/15g52uf9/ekali-awakening-mix-7-2019-04-16.html',
 'https://www.1001tracklists.com/tracklist/2vgpzuft/ekali-siam-songkran-music-festival-thailand-2019-04-14.html',
 'https://www.1001tracklists.com/tracklist/2n07hdxk/ekali-mad-hatters-castle-beyond-wonderland-united-states-2019-03-23.html',
 'https://www.1001tracklists.com/tracklist/2bq5p4f1/ekali-cold-blue-night-owl-radio-187-2019-03-22.html',
 'https://www.1001tracklists.com/tracklist/2wd8ru3k/ekali-orlando-amphitheater-united-states-2019-02-02.html',
 'https://www.1001tracklists.com/tracklist/1fu7gjj9/louis-the-child-ekali-whethan-melvv-holy-ship-playground-set-united-states-2019-01-11.html',
 'https://www.1001tracklists.com/tracklist/1878qp09/ekali-holy-ship-day-2-united-states-2019-01-10.html',
 'https://www.1001tracklists.com/tracklist/1s1x3969/ekali-pool-deck-holy-ship-united-states-2019-01-09.html',
 'https://www.1001tracklists.com/tracklist/1957ncdk/ekali-supernova-stage-lights-all-night-united-states-2018-12-29.html',
 'https://www.1001tracklists.com/tracklist/j0b62dk/ekali-awakening-mix-6-2018-12-17.html',
 'https://www.1001tracklists.com/tracklist/zuwch91/ekali-kineticfield-edc-china-guangdong-2018-11-24.html',
 'https://www.1001tracklists.com/tracklist/179cxnvt/ekali-crystal-eyes-tour-the-sinclair-boston-united-states-2018-11-08.html',
 'https://www.1001tracklists.com/tracklist/2l44qn0t/ekali-awakening-radio-004-2018-11-06.html',
 'https://www.1001tracklists.com/tracklist/2cmp4x41/ekali-the-sauce-pres.-by-thissongissick-vol.-005-2018-10-25.html',
 'https://www.1001tracklists.com/tracklist/bfbcrd1/ekali-awakening-radio-003-2018-10-23.html',
 'https://www.1001tracklists.com/tracklist/12n4qbw9/ekali-awakening-radio-002-2018-10-09.html',
 'https://www.1001tracklists.com/tracklist/20ft0sp1/ekali-awakening-radio-001-2018-09-25.html',
 'https://www.1001tracklists.com/tracklist/u7r8cw1/ekali-perrys-stage-lollapalooza-united-states-2018-08-05.html',
 'https://www.1001tracklists.com/tracklist/1mdf4gw1/ekali-corona-electric-beach-stage-hard-summer-festival-united-states-2018-08-04.html',
 'https://www.1001tracklists.com/tracklist/28tsq9x9/ekali-organ-of-harmony-stage-tomorrowland-weekend-1-belgium-2018-07-20.html',
 'https://www.1001tracklists.com/tracklist/v5f7w1t/4b-ekali-night-owl-radio-150-2018-07-07.html',
 'https://www.1001tracklists.com/tracklist/1vsgmzm9/ekali-awakening-mix-5-2018-06-25.html',
 'https://www.1001tracklists.com/tracklist/26y0v4jk/ekali-mainstage-nameless-music-festival-italy-2018-06-01.html',
 'https://www.1001tracklists.com/tracklist/15f3cr59/ekali-cosmicmeadow-edc-las-vegas-united-states-2018-05-19.html',
 'https://www.1001tracklists.com/tracklist/hzlg041/tiesto-ekali-club-life-577-2018-04-21.html',
 'https://www.1001tracklists.com/tracklist/9gz7gy9/ekali-sahara-tent-coachella-festival-weekend-2-united-states-2018-04-21.html',
 'https://www.1001tracklists.com/tracklist/jxk3ppk/ekali-do-lab-stage-coachella-festival-united-states-2018-04-14.html',
 'https://www.1001tracklists.com/tracklist/1uuh00bk/ekali-sahara-tent-coachella-festival-weekend-1-united-states-2018-04-14.html',
 'https://www.1001tracklists.com/tracklist/186d15n9/ekali-brownies-and-lemonade-stage-ultra-music-festival-miami-miami-music-week-united-states-2018-03-24.html',
 'https://www.1001tracklists.com/tracklist/1zhb13zk/ekali-awakening-mix-4-2018-02-12.html']

#useful packages for recommendation engines? 
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from pyspark import SparkContext,StorageLevel
from pyspark.mllib.feature import Word2Vec,Word2VecModel
#x_train, x_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.3, random_state = 0)
"""