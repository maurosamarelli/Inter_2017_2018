import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

def normalize_column(data, column_list):
    '''
        questa funzione consente di normalizzare le colonne memorizzate come json all'interno di un dataframe
        parametri:
        1) data: dataframe con colonne da normalizzare
        2) column_list: lista delle colonne da normalizzare
    '''
    for column in column_list:
        nested_df = json_normalize(data=data[column]).reset_index(drop=True).add_prefix(column + "_")
        data = pd.concat([data.reset_index(drop=True).drop(column, axis=1), nested_df], axis=1)
    return data

def decode_string(data, column_list):
    '''
        questa funzione consente di decodificare i caratteri speciali contenuti in una colonna di tipo stringa
        parametri:
        1) data: dataframe con colonne da decodificare
        2) column_list: lista delle colonne da decodificare
    '''
    for column in column_list:
        l = []
        for s in data[column]:
            l.append(s.encode().decode('unicode-escape'))
        data[column] = pd.Series(l)
    return data

def get_referees(data, column):
    '''
        questa funzione consente di spacchettare i dati relativi agli arbitri dei match creando opportune colonne nel dataframe
        parametri:
        1) data: dataframe con i dati relativi ai match
        2) column: nome della colonna contenente i dati degli arbitri
    '''
    referee, firstAssistant, secondAssistant, fourthOfficial, firstAdditionalAssistant,  secondAdditionalAssistant = [], [], [], [], [], []
    for match in data[column]:
        for ref in match:
            if ref['role'] == "referee":
                referee.append(ref['refereeId'])
            elif ref['role'] == "firstAssistant":
                firstAssistant.append(ref['refereeId'])
            elif ref['role'] == "secondAssistant":
                secondAssistant.append(ref['refereeId'])
            elif ref['role'] == "fourthOfficial":
                fourthOfficial.append(ref['refereeId'])
            elif ref['role'] == "firstAdditionalAssistant":
                firstAdditionalAssistant.append(ref['refereeId'])
            elif ref['role'] == "secondAdditionalAssistant":
                secondAdditionalAssistant.append(ref['refereeId'])
        n_referees = max(len(referee), len(firstAssistant), len(secondAssistant), len(fourthOfficial), len(firstAdditionalAssistant), len(secondAdditionalAssistant))
        if len(referee) != n_referees:
            referee.append('')
        if len(firstAssistant) != n_referees:
            firstAssistant.append('')
        if len(secondAssistant) != n_referees:
            secondAssistant.append('')
        if len(fourthOfficial) != n_referees:
            fourthOfficial.append('')
        if len(firstAdditionalAssistant) != n_referees:
            firstAdditionalAssistant.append('')
        if len(secondAdditionalAssistant) != n_referees:
            secondAdditionalAssistant.append('')
    data = data.reset_index(drop=True)
    data['referee'] = pd.Series(referee).astype(object)
    data['firstAssistant'] = pd.Series(firstAssistant).astype(object)
    data['secondAssistant'] = pd.Series(secondAssistant).astype(object)
    data['fourthOfficial'] = pd.Series(fourthOfficial).astype(object)
    data['firstAdditionalAssistant'] = pd.Series(firstAdditionalAssistant).astype(object)
    data['secondAdditionalAssistant'] = pd.Series(secondAdditionalAssistant).astype(object)
    data.drop(column, axis=1, inplace=True)
    return data

def get_teamsData(data):
    '''
        questa funzione consente di ottenere un dizionario che memorizza i dati dei team per ogni match
        parametri:
        1) data: dataframe con i dati relativi ai match
    '''
    teamsData = dict()
    for i in range(len(data)):
        df = pd.DataFrame(data.iloc[i].teamsData)
        df.columns = [df.loc["side"][0], df.loc["side"][1]]
        teamsData[data.iloc[i].wyId] = df
    return teamsData

def get_formations(teamsData):
    '''
        questa funzione consente di ottenere un dataframe contenente per ogni match la lista della lineup con eventuali sostituzioni
        parametri:
        1) teamsData: dataframe relativo ai dati del team per ogni match
    '''
    df = pd.DataFrame()
    for matchId in teamsData.keys():
        for team in ['home', 'away']:
            lineup = pd.DataFrame(teamsData[matchId].loc["formation"][team]['lineup'])
            lineup['matchId'] = matchId
            lineup['team'] = team
            subs = pd.DataFrame(teamsData[matchId].loc["formation"][team]['substitutions'])
            aux = pd.merge(lineup, subs, how="left", left_on="playerId", right_on="playerOut").drop("playerOut", axis=1)
            aux.minute = aux.minute.astype(object)
            aux.playerIn = aux.playerIn.astype(object)
            df = pd.concat([df, aux])
    return df

def get_event_locations(data, column):
    '''
        questa funzione consente di spacchettare i dati relativi a posizione di partenza e posizione di arrivo per ogni evento di ogni match
        parametri:
        1) data: dataframe relativo ai dati degli eventi dei match
        2) column: nome colonna in cui sono memorizzati i dati delle posizioni riferite all'evento
    '''
    x_start, y_start, x_end, y_end = [], [], [], []
    for location in data[column]:
        if len(location)==2:
            x_start.append(location[0]['x'])
            y_start.append(location[0]['y'])
            x_end.append(location[1]['x'])
            y_end.append(location[1]['y'])
        elif len(location)==1:
            x_start.append(location[0]['x'])
            y_start.append(location[0]['y'])
            x_end.append("")
            y_end.append("")
    data = data.reset_index(drop=True)
    data['x_start'] = pd.Series(x_start)
    data['y_start'] = pd.Series(y_start)
    data['x_end'] = pd.Series(x_end)
    data['y_end'] = pd.Series(y_end)
    data.drop(column, axis=1, inplace=True)
    return data

def get_event_tags(data, column):
    '''
        questa funzione consente di spacchettare i tag associati agli eventi di un match e di creare una colonna per ogni tag
        per ogni evento, si attribuisce "yes" alle colonne dei tag associato all'evento e "no" alle colonne dei tag non associati all'evento
        la funzione utilizza un dizionario avente come chiavi i codici dei tag e come valori le descrizione dei tag
        le descrizioni dei tag diventano i nomi delle colonne aggiunte nel dataframe
        il dizionario si basa sulla documentazione consultabile al link apidocs.wyscout.com
    '''
    tags_dict = dict()
    tags_dict[101] = "goal"
    tags_dict[102] = "own_goal"
    tags_dict[301] = "assist"
    tags_dict[302] = "key_pass"
    tags_dict[1901] = "counter_attack"
    tags_dict[401] = "left_foot"
    tags_dict[402] = "right_foot"
    tags_dict[403] = "head_body"
    tags_dict[1101] = "direct"
    tags_dict[1102] = "indirect"
    tags_dict[2001] = "dangerous_ball_lost"
    tags_dict[2101] = "blocked"
    tags_dict[801] = "high"
    tags_dict[802] = "low"
    tags_dict[1401] = "interception"
    tags_dict[1501] = "clearance"
    tags_dict[201] = "opportunity"
    tags_dict[1301] = "feint"
    tags_dict[1302] = "missed_ball"
    tags_dict[501] = "free_space_right"
    tags_dict[502] = "free_space_left"
    tags_dict[503] = "take_on_left"
    tags_dict[504] = "take_on_right"
    tags_dict[1601] = "sliding_tackle"
    tags_dict[601] = "anticipated"
    tags_dict[602] = "anticipation"
    tags_dict[1701] = "red_card"
    tags_dict[1702] = "yellow_card"
    tags_dict[1703] = "second_yellow_card"
    tags_dict[1201] = "goal_low_center"
    tags_dict[1202] = "goal_low_right"
    tags_dict[1203] = "goal_center"
    tags_dict[1204] = "goal_center_left"
    tags_dict[1205] = "goal_low_left"
    tags_dict[1206] = "goal_center_right"
    tags_dict[1207] = "goal_high_center"
    tags_dict[1208] = "goal_high_left"
    tags_dict[1209] = "goal_high_right"
    tags_dict[1210] = "out_low_right"
    tags_dict[1211] = "out_center_left"
    tags_dict[1212] = "out_low_left"
    tags_dict[1213] = "out_center_right"
    tags_dict[1214] = "out_high_center"
    tags_dict[1215] = "out_high_left"
    tags_dict[1216] = "out_high_right"
    tags_dict[1217] = "post_low_right"
    tags_dict[1218] = "post_center_left"
    tags_dict[1219] = "post_low_left"
    tags_dict[1220] = "post_center_right"
    tags_dict[1221] = "post_high_center"
    tags_dict[1222] = "post_high_left"
    tags_dict[1223] = "post_high_right"
    tags_dict[901] = "through"
    tags_dict[1001] = "fairplay"
    tags_dict[701] = "lost"
    tags_dict[702] = "neutral"
    tags_dict[703] = "won"
    tags_dict[1801] = "accurate"
    tags_dict[1802] = "not_accurate"
    
    for tag in tags_dict.keys():
        flag = []
        for list_tags in data[column]:
            x = "no"
            for el in list_tags:
                if el["id"] == tag:
                    x = "yes"
            flag.append(x)
        data = data.reset_index(drop=True)
        data[tags_dict[tag]] = pd.Series(flag)
                
    data.drop(column, axis=1, inplace=True)
    return data