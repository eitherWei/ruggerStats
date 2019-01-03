import requests
import json
import re
import pprint





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

def getGameMetaData(stats):
    metaDict = {}
    print(stats.keys())
#    print(stats['gamePackage'])
    ## iterated as far as gamePackage all empty
#    print(pprint.pprint(stats['gamePackage']))

    datum = stats['gamePackage']
    print(type(datum))
    import pandas as pd

    #df = pd.DataFrame(datum)
    #print(df.head())

    #print(len(datum.keys()))
    #print(datum.keys())
    #print(10*"-")
    #print(datum['matchEvents'].keys())


    #print(10*"=")
    #print(datum['matchEvents']['col'])
    #print(10*"*")
    #print(datum['matchAttacking'].keys())
    #print(10*"attacking~")
    #print(datum['matchAttacking']['col'])
    #print(10*"~~")
    #print(datum.keys())
    #print(10*"# # ")
    #print(datum[list(datum.keys())[18]])
    #print(list(datum.keys())[18])
    #print("--"*10)
    #num = 23
    #print(datum[list(datum.keys())[num]])
    #print(10*("&&"))
    #print(list(datum.keys())[num])
    ##matchLineUp == full list of all players
    print("\n")
    print("------------------------------")
    print("matchEvents")
    print("------------------------------")
    print("\n\n\n")
    d = extractmatchEvents(datum['matchEvents'])
    #print(d)


def extractmatchEvents(datum):
    # keys found in matchEvents
#    print(datum.keys())
    # drill into the key column  - it contains the matchEvent of interest
    d = datum['col']
    # examine the keys for areas of interest
    #print(type(d))
    print(10*"== zero ==")

    d_0 = d[0]
    print(len(d_0))
    print(d_0)
    print(50*"=")
    print("\n")


    ## module drills into text found in the first list and retrieves
    ## number of tries in the game
    #trydata = type(k['data'][0])
#    print(type(trydata))
    ## key is made up of type/data - we are interested in data
    k = list(d_0)
    trydata = k[0]['data']
    print(len(trydata))
    for event in trydata:
        print(event['text'])
        print(event.values())
        print("\n")
    #print(type(trydata))
    #print(trydata.keys())
    #print(trydata['text'])

    '''
    print(10*"== one =")
    d_1 = d[1]

    print(len(d_1))

    print(10*"-- a --")
    print(type(d_1[0]))
    print(d_1[0].keys())

    print(10*"-- b --")
    print(d_1[1].keys())
    print(type(d_1[1]))
    '''

    return d




    #print(datum['matchDetails']['Game Info'])


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
