import requests
import json
import re





def getMetaData(url):
    # link to original data - will need to be taken in as a dynamic input
    print(url)
    #url = "http://www.espn.co.uk/rugby/playerstats?gameId=293905&league=289234"
    #url = "http://www.espn.com.au/rugby/match?gameId=293902&league=289234"
    ## retrieve the data in question : will appear as a <response + [code]>
    html_doc = requests.get(url)

    # parses the data based on below identified section which is where are data lives returns a dictionary
    stats = json.loads(re.search(r"window.__INITIAL_STATE__\s*=\s*({.*});",html_doc.text).group(1))
    return stats
# extract player details
def extractPlayerDeets(stats, num, HA): # stats is the original dictionary: num is a [1-15] of starting players: HA relates to home or away team
    attri = list(stats['gamePackage']['matchLineUp'][HA]['team'])
    #print(stats['gamePackage']['matchLineUp']['home'].keys())
    #print(len(stats['gamePackage']['matchLineUp']['home']['team']))
    playerValues = [] # a list to store the player performance deets
    attriHeads = list(attri[0].keys()) # names of all stats on player recorded
#    num = 2
    # first 12 attributes are strings and can be analysed later
    # num is used to iterate over which player to choose
    name = attri[num][attriHeads[2]] ## attri[i] reveals the name of the player in question
    #print(name)
    for number in range(0, len(attriHeads)):
        #print(attri[num][attriHeads[number]])
        # formating the data to allow for the dictionary in the input dictionary
        if isinstance(attri[num][attriHeads[number]],dict):
            #print(list(attri[num][attriHeads[number]].values())[0])
            # xheck to see if the player had any events
            if(attri[num][attriHeads[number]].values()):
                playerValues.append(list(attri[num][attriHeads[number]].values())[0])
            else:
                # if the player had no events then add a generic placeholder
                playerValues.append("_")
        else:
            #print(attri[num][attriHeads[number]])
            # standard string input store are normal
            playerValues.append(attri[num][attriHeads[number]])

    return(name , playerValues, attriHeads)


def gameMetaData(stats):
    metaDict = {}
    metaDict['home'] = stats['gamePackage']['headToHead']['data'][0]['home']['name']
    metaDict['away'] = stats['gamePackage']['headToHead']['data'][0]['away']['name']
    metaDict['score'] = stats['gamePackage']['headToHead']['data'][0]['score']
    return metaDict


def extractAllPlayers(stats, HA):
    playerList = []
    # method loops over json and returns the score of the game
    gameOutComeDict = gameMetaData(stats)
    for i in range(15):
        # returns return(name , playerValues, attriHeads)
        value = extractPlayerDeets(stats, i, HA)
        # append the score to the end of each player result
        value[1].append(gameOutComeDict['score'])
        # append the score to the end of each player result
        # hammy way of extending the input list to have extra detail
        # TODO create additional tables 
        value[2].append('finalScore')
        # append the final list to the team list
        playerList.append(value[1])
    return (playerList , value[2])



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
