# Inter_2017_2018
Data analysis about Football Club Internazionale season 2017-2018, i.e. when we came back to the UCL!

In this repository we handle [Wyscout](https://wyscout.com/) data and to extract useful information for the tactical point of view.

We use the [Player Rank](https://github.com/mesosbrodleto/playerank) open source project owned by Pappalardo Luca, Cintia Paolo & Co.

In particulary, json files about soccer data can be downloaded executing data_download.py in [Player Rank](https://github.com/mesosbrodleto/playerank)

Notebook Description:

01 players.ipynb: get and explore data about inter players

02 team.ipynb: get and explore data about inter team

03 matches.ipynb: get and explore data about inter matches

04 events.ipynb: get and explore data about inter matches events

05 pass_analysis.ipynb
  - count of total passes for each player in each match
  - calculate pass accuracy for each player in each match
  - calculate forward pass percentage for each player in each match
  - focus on Brozovic: count of total passes evolution during the season
  - focus on Brozovic: pass accuracy evolution during the season
  - focus on Brozovic: forward pass evolution during the season
  - rank players by number of total passes in the season
  - rank players by pass accuracy in the season
  - rank players by forward pass percentage in the season

06 ball_possession_analysis.ipynb
  - develop a function which is able to calculate time possession of a team, time possession of the opponent, time ball duels and time stopped
  - calculate ball possession percentage for each match
  - evolution of ball possession percentage during the season
