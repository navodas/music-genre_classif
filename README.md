## Music genre classification

This project consists of three main parts.
1. Using Spotify API to access audio features about the tracks belong to 10 major music genres (data_extractor.py).
2. Writing extracted data into a Postgress DB (data_extractor.py, connect.py, config.py).
3. Using extracted data for EDA and training a ML classifier for genre classification (music-genre-prediction.ipynb).

In order to execute the code you need to create below files.

1.client_info.txt - This contains API keys  to connec to Spotify web API.

Client ID : xxxxxxxxxxxxxxxxxxx

Client Secret : xxxxxxxxxxxxxxxxxxx

2. database.ini - This contains database connection string if you want to write the collected data to a Postgress DB.

[postgresql]
host=<host name or ip of the database machine i.e., localhost>
database=<name of the database i.e., spotify>
user=<user i.e.,postgres>
password=<password>
port = <database port i.e., 5432>

### Execution

The req.txt contains all the required packages.

####To acccess Spotify API for gathering data
python3 data_extractor.py 

####Data analysis and ML
music-genre-prediction.ipynb