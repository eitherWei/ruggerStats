import requests
import json
import re

def getMetaData():
    # link to original data - will need to be taken in as a dynamic input
    url = "http://www.espn.co.uk/rugby/playerstats?gameId=293905&league=289234"

    ## retrieve the data in question : will appear as a <response + [code]>
    html_doc = requests.get(url)

    # parses the data based on below identified section which is where are data lives returns a dictionary
    stats = json.loads(re.search(r"window.__INITIAL_STATE__\s*=\s*({.*});",html_doc.text).group(1))
    return stats
# extract player details
def extractPlayerDeets(stats, num, HA): # stats is the original dictionary: num is a [1-15] of starting players: HA relates to home or away team
    attri = list(stats['gamePackage']['matchLineUp'][HA]['team'])

    playerValues = [] # a list to store the player performance deets
    attriHeads = list(attri[0].keys()) # names of all stats on player recorded

    # first 12 attributes are strings and can be analysed later
    name = attri[num][attriHeads[2]] ## attri[i] reveals the name of the player in question
    for number in range(0, len(attriHeads)):
        if isinstance(attri[num][attriHeads[number]],dict):
            #print(list(attri[num][attriHeads[number]].values())[0])
            playerValues.append(list(attri[num][attriHeads[number]].values())[0])
        else:
            #print(attri[num][attriHeads[number]])
            playerValues.append(attri[num][attriHeads[number]])

    return(name , playerValues, attriHeads)

#######################################################
# running the above code
#######################################################

'''
num = 3
HA = "away"
k, v, colheads = extractPlayerDeets(stats, num, HA)

print(k)
print(10*"-")
print(v)
print(10*"-")
print(colheads)
print(10*"-")
'''
