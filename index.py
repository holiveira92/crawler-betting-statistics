import json
import requests
from bs4 import BeautifulSoup

def getDataByUrlTeam(html_text, team_name):
    # Definindo variáveis necessárias e objetos
    soup = BeautifulSoup(html_text, 'html.parser')

    # Definindo área do DOM que contém as informações desejadas
    tables = soup.find_all("table", {"cellspacing":"0", "cellpadding":"1", "bgcolor":"#f8f8f8", "width":"99%"})
    
    first_goal = getDataByKey(tables, "Team scored first")
    half_time_leading = getDataByKey(tables, "Team was leading at half-time")
    opponent_scored_first = getDataByKey(tables, "Opponent scored first")
    opponent_leading_ht = getDataByKey(tables, "Opponent was leading at half-time")
    
    return {
        'team_name': team_name,
        'first_goal_general' : getDataByArrayIndex(first_goal, 0),
        'first_goal_home' : getDataByArrayIndex(first_goal, 1),
        'first_goal_away' : getDataByArrayIndex(first_goal, 2),
        'half_time_leading_general' : getDataByArrayIndex(half_time_leading, 0),
        'half_time_leading_home' : getDataByArrayIndex(half_time_leading, 1),
        'half_time_leading_away' : getDataByArrayIndex(half_time_leading, 2),
        'opponent_scored_first_general' : getDataByArrayIndex(opponent_scored_first, 0),
        'opponent_scored_first_home' : getDataByArrayIndex(opponent_scored_first, 1),
        'opponent_scored_first_away' : getDataByArrayIndex(opponent_scored_first, 2),
        'opponent_leading_half_time_general' : getDataByArrayIndex(opponent_leading_ht, 0),
        'opponent_leading_half_time_home' : getDataByArrayIndex(opponent_leading_ht, 1),
        'opponent_leading_half_time_away' : getDataByArrayIndex(opponent_leading_ht, 2),
    }

def getDataByKey(tables, key):
    response = [] # [0] => Total , [1] => Home, [2] => Away
    # itera nos itens encontrados na página
    for table in tables:
        row = ''
        tr_rows = table.findAll('tr')
        for tr_row in tr_rows:
            if(tr_row.text.find(key) > -1):
                percentage_position_array = 2
                response.append(
                    tr_row.findAll("td")[percentage_position_array].text.replace("%", "")
                )
    return response

def loadTeamsList():
    # JSON file
    f = open ("teams_list_url.json", "r")
    
    # Reading from file
    data = json.loads(f.read())
    
    # Closing file
    f.close()
    
    return data

def writeJsonFile(json_final_data):
    json_final_data = json.dumps(json_final_data)
    with open('output.json', 'w') as outfile:
        outfile.write(json_final_data)
    
def executeCrawler(teams_list):
    json_final_data = []
    list_qty = len(teams_list)
    count = 1
    for team_name in teams_list:
        json_data = requests.get(teams_list[team_name]).text
        output_data = getDataByUrlTeam(json_data, team_name)
        print("------------------------------------------------------------------------------------------------------");
        print( str(count) + "/" + str(list_qty))
        print( team_name + " :" )
        print( output_data )
        print("------------------------------------------------------------------------------------------------------");
        
        json_final_data.append( output_data )
        count = count + 1
    
    writeJsonFile(json_final_data)

def getDataByArrayIndex(arr, index):
    if ( index < len(arr) ) :
        return arr[index]
    else :
        return 0
    
# Início da execução do script
teams_list = loadTeamsList()
executeCrawler(teams_list)
