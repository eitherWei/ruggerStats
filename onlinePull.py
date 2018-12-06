import requests
import json
import re
import pandas as pd

url = "http://www.espn.co.uk/rugby/playerstats?gameId=293905&league=289234"
html_doc = requests.get(url)
print(html_doc)


stats = json.loads(re.search(r"window.__INITIAL_STATE__\s*=\s*({.*});",html_doc.text).group(1))

#stats = json.load(re.search(r"window.__INITIAL_STATE__\s*=\s*({.*});", html_doc.text).group(1))

#print(type(stats))
#print(stats.keys())

#print(stats['gamePackage'].keys())

for player in stats['gamePackage']['matchLineUp']:
    try:
        print(player)
        print(stats['gamePackage']['matchLineUp'][player].keys())
        print("^^^^^^^^^^^^^^^^^^^^")
    except:
        a = 2



#print(10*"+")
#print(type(stats['gamePackage']['matchLineUp']['text']['scoring']))
#print(stats['gamePackage']['matchLineUp']['text']['attacking'])
#columns = list(stats['gamePackage']['matchLineUp']['home']['team'][0].keys())
#rows = stats['gamePackage']['matchLineUp']['home']['team'][0]['name']
#print(columns)
#print(rows)


def determineRows(stats):
    columns = list(stats['gamePackage']['matchLineUp']['home']['team'][0].keys())
    rows = stats['gamePackage']['matchLineUp']['home']['team']
    playerList = []
    for player in rows:
        #print(player['name'])
        playerList.append(player['name'])

    return playerList

def extractPlayerDeets(stats, num, HA):
    #columns = stats['gamePackage']['matchLineUp']['home']['team']
    attri = list(stats['gamePackage']['matchLineUp'][HA]['team'])
    #print(attri[0]['id'])
    #print(10*"#")
    # each attribbute in the list is a dictionary
    #playerKey = []
    playerValue = []
    # extracts the list of attribute headings to be extracted
    attriHeads = list(attri[0].keys()) # this should give us the column names for identifying which values to take out
    #playerDeets = []
    print(attriHeads[num])
    name = attri[num][attriHeads[2]] ## attri[i] reveals the name of the player in question
    for number in range(12, len(attriHeads)):
        #print(type(attri[0][attriHeads[number]]))
        #print(attri[num][attriHeads[number]]['name']) # iterates over all of the attributes
        #print(attri[0][attriHeads[number]]['value'])
        #print(10 * "%")
        #playerKey.append(attri[num][attriHeads[number]]['name'])
        playerValue.append(attri[num][attriHeads[number]]['value'])
        #print(attri[num][attriHeads[number]]['name'])
        #print(playerValue.append(attri[num][attriHeads[number]]['value']))
        #print(attri[attriHeads[number]])

    return (name , playerValue)

num = 3
HA = "away" ## HA is boolean that determines wether we are looking at home or away
for i in range(0, 14):
    k, v = extractPlayerDeets(stats, i, HA)
    print(k)
    print(v)
'''
print(10* "+")
print(len(k))
print(len(v))

print(k)
print(type(k))
print(v)
print(type(v))

rows = determineRows(stats)
print(rows)
columns = columns = list(stats['gamePackage']['matchLineUp']['home']['team'][0].keys())
## create the dataframe to hold the game stats
df = pd.DataFrame(columns = columns, index = rows)
print(df.head())
print(df.columns)

attri = list(stats['gamePackage']['matchLineUp']['home']['team'])

print(10*"==")
extraAttributes = ['name', 'number', 'position', 'homeAway', 'onPitch']
attributes = extraAttributes + k
print(attributes)
'''
