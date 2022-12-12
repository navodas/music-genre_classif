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



import json
with open('genre.json', 'w') as fp:
    json.dump(genre_dict, fp)