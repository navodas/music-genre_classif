from distutils.command.config import config
from tkinter import NUMERIC
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import glob
import os
import json
import time
from sqlalchemy import create_engine
from connect import *
import requests

def authorization_spotify():
    #Read API key
    with open('client_info.txt') as f:
        lines = f.readlines()

    #Authentication - without user
    cid= lines[0].split(":")[1].strip()
    secret =lines[1].split(":")[1].strip()

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager, status_retries=5)

    return sp

#Read json file that contains different music genres and their sub-genres
def read_genre_list():
    with open('genre.json') as f:
        genre_dict = json.load(f)
    return genre_dict

def get_playlist(spotify_object, sub_genre):
    play_lists = spotify_object.search(sub_genre, type='playlist', limit=10)
    play_lists = pd.DataFrame(play_lists['playlists']['items'])
    play_lists = play_lists['id'] 
    return  play_lists  

def get_track_info(spotify_object, play_list, cnt):
    t_data = None
    t_data=spotify_object.playlist_items(play_list)['items'][cnt]['track'] 

    if t_data == None :
        track_id, track_popularity = None, None
    else:
        track_id = t_data['id']
        track_popularity = t_data['popularity']

    return track_id, track_popularity

def get_track_audio_features(spotify_object, track_id):
    audio_df = pd.DataFrame(spotify_object.audio_features(track_id))

    #only the require features, remove 'type', 'uri', 'track_href', 'analysis_url', 
    #audio_df = audio_df['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'id', 'duration_ms','time_signature']
    return audio_df

def reconnect_to_spotify():
    print("Reconnect to Spotify...")
    time.sleep(np.random.uniform(2, 5))
    sp= None
    count=0
    while sp == None:
        if count < 10:
            sp = authorization_spotify()   
            count += 1
        else:
            break;

    return sp

def write_csv(df, fname):
    df.to_csv(fname, index=False)

#Data extraction function
#1. For each genre-sub-genre combination get first three palylist ids.
#2. For each playlist get the respective track-ids
#3. For each track extract their audiofeatures and popularity

def extract_spotify_data(sp) :

    track_feat_df = pd.DataFrame()

    #Establishing the connection to db and create table if not exists
    create_table()


    for g in tqdm(genre_dict.keys()):
        
        for sg in genre_dict[g]:

            print("Genre : ",g, "Sub-genre : ", sg)

            play_lists = []

            #get playlist ids
            try:
                play_lists = get_playlist(spotify_object=sp, sub_genre=sg)
            except (Exception, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as error:
                sp = reconnect_to_spotify()
                play_lists = get_playlist(spotify_object=sp, sub_genre=sg)

          #no playlists returened
            if len(play_lists) < 1:
                print("No playlists found for sub-genre!")
                break;

            play_list_tracks=pd.DataFrame()
            #get track ids
            for p in play_lists:
                try:
                    n_items = len(sp.playlist_items(p)['items'])
                except (Exception, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as error:   
                    sp = reconnect_to_spotify()
                    n_items = len(sp.playlist_items(p)['items'])

                #for each track in playlist
                for n in range(1, n_items):
                    track_id, track_popularity = None, None
                    #get general track info
                    try:
                        track_id, track_popularity = get_track_info(spotify_object=sp, play_list=p, cnt=n)
                    except (Exception, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as error:   
                        sp = reconnect_to_spotify()
                        track_id, track_popularity = get_track_info(spotify_object=sp, play_list=p, cnt=n)
                    
                    if ((track_id is not None)  &  (track_popularity is not None)):
                        #get track's audio features
                        try: 
                            audio_df = get_track_audio_features(sp, track_id)
                            
                        except (Exception, requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as error:  
                            sp = reconnect_to_spotify()       
                            audio_df = get_track_audio_features(sp, track_id)                  


                        audio_df['popularity'] = track_popularity
                        audio_df['genre'] = g
                        audio_df['sub-genre'] = sg

                        play_list_tracks = pd.concat([play_list_tracks, audio_df])

                        time.sleep(np.random.uniform(1, 3))
                    else:
                        print("Unable to retrieve track data. Skip this track..")
                    

            print(play_list_tracks)
            #write_to_db(play_list_tracks)
            fname=str(g)+'.csv'
            write_csv(play_list_tracks,fname)

#Connect to Spotify API
sp = authorization_spotify()

#Read genre list
genre_dict = read_genre_list()

#Get Spotify data
extract_spotify_data(sp)