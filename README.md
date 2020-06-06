# Inter_2017_2018
Data analysis about Football Club Internazionale season 2017-2018, i.e. when we came back to the UCL!

This repository uses [Wyscout](https://wyscout.com/) data to extract useful information for the tactical point of view.

Dataset Links
'matches' : 'https://ndownloader.figshare.com/files/14464622',
'events' : 'https://ndownloader.figshare.com/files/14464685',
'players' : 'https://ndownloader.figshare.com/files/15073721',
'teams': 'https://ndownloader.figshare.com/files/15073697',

Notebook Descriptions:

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
  - focus on Brozovic: forward pass percentage evolution during the season
  - rank players by number of total passes in the season
  - rank players by pass accuracy in the season
  - rank players by forward pass percentage in the season

06 ball_possession_analysis.ipynb
  - develop a function which is able to calculate time possession of a team, time possession of the opponent, time ball duels and time stopped
  - calculate ball possession percentage for each match
  - evolution of ball possession percentage during the season
  - calculate ball possession percentage in the opponent half pitch
  - evolution of ball possession percentage in the opponent half pitch during the season
  - calculate harmonic mean between ball possession percentage and ball possession percentage in the opponent field (dangerousness of the possession)
  - rank matches by ball possession percentage
  - rank matches by ball possession percentage in the opponent field
  - rank matches by dangerousness of the possession
  
 07 shot_analysis.ipynb
  - rank players by number of total shots in the season
  - rank players by number of goals in the season
  - rank players by number of shots per goal or by number of percentage of goal on shots
