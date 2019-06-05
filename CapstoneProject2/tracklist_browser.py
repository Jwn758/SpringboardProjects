# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 12:55:09 2019

@author: A0709761
"""

#Importing relevant modules
import pandas as pd
import unicodedata
from urllib.request import Request, urlopen
import os
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#importing relevant packages for automated web navigation
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#from splinter import Browser
#from splinter.exceptions import ElementDoesNotExist
#Importing outputs from 'spotifyxx_v4.py' to obtain Spotify User's top artists, top song names, and edm Artists
from spotifyxx_v4 import unique_artists, unique_songs, unique_edmArtists

#Ways to avoid 1001tracklists.com banning web scraper
"""
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
headers={'User-Agent':user_agent,} 
"""


"""


#define artist to be looked up
artistname = 'Ekali'

#Intializing webpage_objects to parse through
TL_webpages_objects = []

#Intializing list to fill in with converted webpage objects into URLs
TL_webpages_names = []

#Filling in TL_webpages_objects and converting to URLs and storing in TL_webpages_names
"""



#Different ways to look up sets to test automated navigator: use all artists (including non-edm artists), use just edm artists, or test artist
"""
#Testing both edm artists and non-edm artists from Spotify User Data
for artist in unique_artists[0:5]:

#Testing for just edm artists from Spotify User Data
for artist in unique_edmArtists[0:5]:

#Testing for just one artist that I picked (Ekali) to work on scraper    
test_artist_list = ["Ekali"]
for artist in test_artist_list:  
"""

"""
#Only using edm artists and only looked up first 5 so I don't get banned from 1001tracklist.com again
#for artist in unique_edmArtists[0:5]:
test_artist_list = ["Ekali"]
for artist in test_artist_list:
    #Go to 1001tracklists.com
    driver.get('http://1001tracklists.com')
    
    #Navigating 1001tracklist.com to search each Artist
    element = driver.find_element_by_name("main_search")
    element.send_keys(artist)
    #implementing wait so I don't get banned again
    element = WebDriverWait(driver, 10)
    
    element = driver.find_element_by_id("searchBtn")
    element.submit()
    
    #Using BeautifulSoup
    
    ###Ways to trick site?
    #req = Request(driver.current_url)
    #page = urlopen(req).read()
    #agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    #page = Request(driver.current_url, headers = agent)
    
    page = urlopen(driver.current_url)
    test_soup = BeautifulSoup(page)
    
    #Find all links and save into list of elements
    TL_webpages_objects = driver.find_elements_by_partial_link_text(artist)
    
    #Bringing search results into list of tracklist names
    for webpage in TL_webpages_objects:
        converted_url = webpage.get_attribute("href")
        TL_webpages_names.append(converted_url)
        
    #Resetting TL_webpages_objects
    TL_webpages_objects = []
"""


"""
###DUPLICATED THIS FROM MAIN.PY FOR JUPYTER NOTEBOOK

#Intializing master dataframe to use for recommendation engine building
Master_DF = pd.DataFrame()

#Going through each imported URL that contains the tracklist of each artist user listens to
for tracklist in TL_webpages_names[0:10]:
    test_page = tracklist
    page = urlopen(test_page)
    test_soup = BeautifulSoup(page)
    get_all_data(test_soup)
    TL_DF = pd.DataFrame.from_records(TL_Data, columns = column_names)
    #Use the code below to combine spotify df with TL DF
    #Master_DF = pd.concat([Master_DF, TL_DF], ignore_index = True)
    Master_DF = TL_DF
"""

#Using Selenium to create driver to navigate web
executable_path = {"executable_path":"/users/jin1/Desktop/Springboard/SpringboardProjects/CapstoneProject2/chromedriver"}
driver = webdriver.Chrome(**executable_path)

#Intializing webpage_objects to parse through
TL_webpages_objects = []
#Intializing list to fill in with converted webpage objects into URLs
TL_webpages_names = []
#Intilaiizing list to fill in with converted webpage objects into URLs AFTER opening Spotify players
TL_final_htmls = []


test_artist_list = ["Ekali"]
for artist in test_artist_list:
#for artist in unique_edmArtists[0:3]:
    #Go to 1001tracklists.com
    driver.get('http://1001tracklists.com')
    
    #Navigating 1001tracklist.com to search each Artist
    element = driver.find_element_by_name("main_search")
    element.send_keys(artist)
    #implementing wait so I don't get banned again
    driver.implicitly_wait(5)
    
    element = driver.find_element_by_id("searchBtn")
    element.submit()
    
    #Using BeautifulSoup
    
    ###Ways to trick site?
    #req = Request(driver.current_url)
    #page = urlopen(req).read()
    #agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    #page = Request(driver.current_url, headers = agent)
    
    
    #Find all links and save into list of elements
    TL_webpages_objects = driver.find_elements_by_partial_link_text(artist)
    
    #Bringing search results into list of tracklist names
    for webpage in TL_webpages_objects:
        converted_url = webpage.get_attribute("href")
        
        #Savings the webpages with opened spotify links
        TL_webpages_names.append(converted_url)
    
    """    
    #Going into each webpage to open up all the spotify links
    driver.get(TL_webpages_names[0])
    WebDriverWait(driver, 10)
    """
    
    ###Going into each webpage to open up all the spotify links
    #for converted_webpage in TL_webpages_names:
    #Only doing 5 for test
    for converted_webpage in TL_webpages_names[0:6]:
        driver.get(converted_webpage)
        driver.implicitly_wait(5)
        
        #Opening up all spotify buttons
        #spotify_buttons = driver.find_elements_by_css_selector('fa fa-24 fa-spotify mediaAction')
        #spotify_buttons = driver.find_elements_by_css_selector("i[onclick*='MediaViewer']")
        spotify_buttons = driver.find_elements_by_css_selector("i[title*='open Spotify player']")
        for button in spotify_buttons:
            try:
                driver.implicitly_wait(15)
                button.click()
            except:
                driver.implicitly_wait(15)
            
        #Savings webpage with opened spotify links
        TL_final_htmls.append(driver.page_source)
        
    #Resetting TL_webpages_objects and TL_webpages_names
    #TL_webpages_objects = []
    #TL_webpages_names = []
    





###Test Code
"""
finaltest_soup = BeautifulSoup(TL_final_htmls[0])
len(finaltest_soup.find_all('iframe', src=re.compile("open.spotify.com/embed/track/")))



from os.path import join
testfile = open(join("/Users/jin1/Desktop/","testfile.txt"), "w+")
testfile.write(TL_final_htmls[0])
testfile.close()

"""

###Test Code
"""
#Search up an artist
element = driver.find_element_by_name("main_search")
element.send_keys(artistname)
element = driver.find_element_by_id("searchBtn")
element.submit()

##Using Splinter
#page = urllib2.urlopen("https://www.1001tracklists.com/tracklist/2l44qn0t/ekali-awakening-radio-004-2018-11-06.html").read()
#page = urllib2.urlopen(browser.url)

#Using BeautifulSoup
page = urlopen(driver.current_url)
test_soup = BeautifulSoup(page)

#Intializing webpage_objects to parse through
TL_webpages_objects = []
#Find all links and save into list of elements
TL_webpages_objects = driver.find_elements_by_partial_link_text(artistname)

#Intializing list to fill in with converted webpage objects into URLs
TL_webpages_names = []

#Bringing search results into list of tracklist names
for webpage in TL_webpages_objects:
    converted_url = webpage.get_attribute("href")
    TL_webpages_names.append(converted_url)
"""
    
