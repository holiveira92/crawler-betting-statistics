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
    
    return json.dumps({
        'first_goal_data' : first_goal_array,
        'half_time_data' : half_time_leading
    })

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


# Início da execução do script
vgm_url = 'https://www.soccerstats.com/team.asp?league=brazil&teamid=1'
json_data = requests.get(vgm_url).text
with open('json_data.json', 'w') as outfile:
    outfile.write(getDataByUrlTeam(json_data))
