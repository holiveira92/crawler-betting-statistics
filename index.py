import json
import requests
from bs4 import BeautifulSoup

def getDataByUrlTeam(html_text):
    # Definindo variáveis necessárias e objetos
    soup = BeautifulSoup(html_text, 'html.parser')

    # Definindo área do DOM que contém as informações desejadas
    tables = soup.find_all("table", {"cellspacing":"0", "cellpadding":"1", "bgcolor":"#f8f8f8", "width":"99%"})
    
    first_goal_array = getFirstGoalData(tables)
    half_time_leading = getHalfTimeLeadingData(tables)
    
    return {
        'first_goal_data' : first_goal_array,
        'half_time_data' : half_time_leading
    }

def getFirstGoalData(tables):
    first_goal_array = [] # [0] => Total , [1] => Home, [2] => Away
    # itera nos itens encontrados na página
    for table in tables:
        row = ''
        tr_rows = table.findAll('tr')
        for tr_row in tr_rows:
            if(tr_row.text.find("Team scored first") > -1):
                percentage_position_array = 2
                first_goal_array.append(
                    tr_row.findAll("td")[percentage_position_array].text.replace("%", "")
                )
    return first_goal_array

def getHalfTimeLeadingData(tables):
    half_time_leading = [] # [0] => Total , [1] => Home, [2] => Away
    # itera nos itens encontrados na página          
    for table in tables:
        row = ''
        tr_rows = table.findAll('tr')
        for tr_row in tr_rows:
            if(tr_row.text.find("Team was leading at half-time") > -1):
                percentage_position_array = 2
                half_time_leading.append(
                    tr_row.findAll("td")[percentage_position_array].text.replace("%", "")
                )
    return half_time_leading


def loadTeamsList():
    # JSON file
    f = open ("teams_list_url.json", "r")
    
    # Reading from file
    data = json.loads(f.read())
    
    # Closing file
    f.close()
    
    return data

def writeJsonFile(team_name, output_data):
    json_final_data = []
    json_final_data.append(json.dumps({
        team_name : output_data
    }))
    
    json_final_data = json.dumps(json_final_data)
    with open(team_name + '.json', 'w') as outfile:
        outfile.write(json_final_data)
    
def executeCrawler(teams_list):
    for team_name in teams_list:
        json_data = requests.get(teams_list[team_name]).text
        output_data = getDataByUrlTeam(json_data)
        print(team_name)
        print(output_data)
        writeJsonFile(team_name, output_data)


# Início da execução do script
teams_list = loadTeamsList()
executeCrawler(teams_list)
