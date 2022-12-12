import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import glob
import os

#Read API key
with open('client_info.txt') as f:
    lines = f.readlines()

#Authentication - without user
cid= lines[0].split(":")[1].strip()
secret =lines[1].split(":")[1].strip()

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# Select a set of genres.
# We select music genres from https://everynoise.com/ which includes only "mainstream" genres sorted by their 
# "popularity". We selected the top  sub-genres for each genre.

genre_dict = { 'pop' : ['pop', 'post-teen pop', 'uk pop',  'dance pop', 'pop dance'], 

'rock': ['rock','album rock', 'permanent wave', 'classic rock','hard rock', 'modern rock', 'alternative rock', 'heartland rock', ],

'hip hop' : ['hip hop', 'rap', 'gangster rap', 'hardcore hip hop', 'east coast hip hop', 'alternative hip hop', 'southern hip hop', 'trap'],

'r&b' : ['r&b', 'urban contemporary', 'contemporary r&b', 'neo soul',  'quiet storm',   'alternative r&b', 'indie r&b'],

'edm ' : ['edm', 'electronica', 'downtempo', 'alternative dance', 'indietronica', 'electropop', 'deep house'],

'country':  ['country',  'contemporary country',  'texas country'],

'classical' : [ 'classical', 'compositional ambient', 'orchestral soundtrack', 'soundtrack'],

'metal' : [ 'metal', 'speed metal', 'old school thrash', 'power metal', 'glam metal', 'alternative metal', 'nu metal', 'screamo', 'metalcore'], 

'jazz' : ['jazz', 'early jazz', 'modern jazz', 'early jazz', 'vocal jazz', 'cool jazz'], 

'blues': ['blues', 'traditional blues', 'acoustic blues', 'texas blues', 'chicago blues', 'memphis blues', 'modern blues', 'country blues', ]}


# Collect playlists, tracks, and audio features per each of the above mentioned genre-subgenre combinations.
# Here we collct the top three play lists for each sub-genre.

track_feat_df = pd.DataFrame()


for g in tqdm(genre_dict.keys()):
    
     for sg in genre_dict[g]:

         print("Genre : ",g, "Sub-genre : ", sg)

         play_lists = []

         #get playlist ids
         play_lists = sp.search(sg, type='playlist', limit=3)
         play_lists = pd.DataFrame(play_lists['playlists']['items'])
         play_lists = play_lists['id']

         #no playlists returened
         if len(play_lists) < 1:
             break;

         #get track ids
         for p in play_lists:
            n_items = len(sp.playlist_items(p)['items'])


            for n in range(1, n_items):
                t_data=sp.playlist_items(p)['items'][n]['track']
                track_id = t_data['id']
                track_popularity = t_data['popularity']

                #get track's audio features
                audio_df = pd.DataFrame(sp.audio_features(track_id))

                audio_df['popularity'] = track_popularity
                audio_df['genre'] = g
                audio_df['sub-genre'] = sg

                #track_feat_df = track_feat_df.append(audio_df,  ignore_index=True)
                track_feat_df = pd.concat([track_feat_df, audio_df])
            
                #time.sleep(np.random.uniform(1, 3))