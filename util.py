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
        questa funzione consente di collezionare i tag (in formato lista) di un evento all'interno di una colonna del dataframe
        parametri:
        1) data: dataframe relativo ai dati degli eventi dei match
        2) column: nome colonna in cui sono memorizzati i tags associati all'evento sottoforma di dizionario
    '''
    tags = []
    for list_tags in data[column]:
        nested_tags = []
        for el in list_tags:
            nested_tags.append(el["id"])
        tags.append(nested_tags)
    data = data.reset_index(drop=True)
    data.drop("tags", axis=1, inplace=True)
    data["tags"] = pd.Series(tags)
    return data    
    
def create_tags_dict():
    '''
        questa funzione consente di creare un dizionario associando ad ogni tag la sua descrizione dell'evento
        please see apidocs.wyscout.com
    '''
    tags_dict = {}
    tags_dict[801] = "high"
    tags_dict[901] = "through"
    tags_dict[1801] = "accurate"
    tags_dict[1802] = "not accurate"
    tags_dict[1001] = "fairplay"
    tags_dict[301] = "assist"
    tags_dict[302] = "key pass"
    tags_dict[1901] = "counter attack"
    tags_dict[401] = "left foot"
    tags_dict[402] = "right foot"
    tags_dict[2001] = "dangerous ball lost"
    tags_dict[403] = "head/body"
    tags_dict[2101] = "blocked"
    tags_dict[1401] = "interception"
    return tags_dict

def label_positive_passes(data, column):
    '''
        questa funzione consente di etichettare un evento (passaggio) se ha avuto esito positivo o negativo (tag=1801)
        parametri:
        1) data: dataframe relativo ai dati degli eventi (passaggi) dei match
        2) column: nome colonna in cui sono memorizzati i tags associati all'evento (passaggio) sottoforma di lista (vedi function get_event_tags)
    '''
    positive = []
    for list_tags in data[column]:
        outcome = "no"
        if list_tags.find('1801') != -1:
            outcome = "yes"
        positive.append(outcome)
    data = data.reset_index(drop=True)
    data["positive"] = pd.Series(positive)
    return data

def gets_unique_tags(data, column):
    '''
        questa funzione consente di ottenere il set di tag univoci presenti negli eventi di un dataframe
        parametri:
        1) data: dataframe relativo ai dati degli eventi dei match
        2) column: nome colonna in cui sono memorizzati i tags associati all'evento sottoforma di lista (vedi function get_event_tags)
    '''
    import itertools
    return set(itertools.chain.from_iterable(data[column]))