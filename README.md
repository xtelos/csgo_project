# CSGO Professional Matches Dataset
### Project Overview:
#### Contributors: Dylan Fodor, Edgar Perez
This project was designed around a dataset we found on Kaggle relating
to the outcomes of CSGO Professional Matches between 2015-2020. Our task
was to take the dataset and load it into a MYSQL relational database, computing
some new and interesting variables that where not present in the pre-existing
dataset.

To run the project, you must download the csv files from the dataset at the link provided
in relevant sources below. You must then place the csv files 
inside a folder named "csgo_data", which will be accessed for data entry 
into the database.

For more info on using MySql with Python and setting up Python-Dotenv, please see
the related links section.

### Database Design:
#### Tables and Related Schemas
- Players (name, team, country, eventID, eventName)
  - Gives an overview of all players, as well
  as the relevant events that they participated in
- Matches (date, matchID, eventID, team1, team2, bestOf, winner)
  - Provides insight on the involved teams in matches, who won, and when
  the match occurred
- Maps (mapName, pickRate, banRate, totalPicks, totalBans)
  - Displays the name of a particular map, as well as its percentage pick/ban rate
  and total number of picks/bans
- Player Analytics (playerName, teamName, matchID, kills, deaths)
  - Gives a summary of a particular player's performance for a particular match

### Interesting Challenges:
##### Calculating Picks / Bans:
When a team wins a match 2-0, they will not go on to play a 3rd map. In these cases,
the 3rd pick and ban column in the CSV (t1_removed_3, t2_removed_3) is 
given '0.0' to represent a map not being picked. To get around this, we simply removed any keys of '0.0' 
from the map dictionaries used. 

##### Calculating the Number of Maps Played in a Match (bestOf):
We also found that the results of matches were incorrect in that if only 1 map was played those
results were listed as a pair (5, 16) for example, which would mean team 1 had won 5 maps, and team 2 had won 16 (which is not correct).
We solved this issue by combining the wins for both teams to equal the maps
played, and if it was higher than 5 (maximum number of maps possible),
we then assumed it was only one map that had been played.

### Relevant Sources and Libraries:
- Kaggle Dataset on CSGO Professional Matches
  - https://www.kaggle.com/mateusdmachado/csgo-professional-matches?select=players.csv
- Python-Dotenv
  - https://github.com/theskumar/python-dotenv
- MySql-Connector-Python
  - https://dev.mysql.com/doc/connector-python/en/
