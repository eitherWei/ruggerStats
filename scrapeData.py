import requests
import json
import re
import pprint


'''
done
    2. Examine prospect of matchSummary  --> examineMatchSummary()
todo:
    1. Take the list of head to heads --> datum[list(datum.keys())[31]] count up the players present. The outcome of the game. Identify if there are certain players that land on the winning side more than others
        --> examineMatchHeadtoHead # not needed for now
    3. matchAwayForm/home 25/22 --> contains the form that the teams are in , could be useful down  the line skip for now

'''
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

    #print(type(datum))
    #print(len(datum.keys()))
    #print("\n")
    #print(50*"%")
    #print(datum.keys())

    for i in range(0, len(datum.keys())):
        print(list(datum.keys())[i])
        print(datum[list(datum.keys())[i]])
        print("i === " + str(i))

        print("\n\n\n")
        print(50*"-")



    d = extractmatchEvents(datum['matchEvents'])
    print(d)
    #print(datum[list(datum.keys())[33]])
    #examineMatchHeadtoHead(datum) ## not needed for now
    extractMatchDiscipline(datum)
    extractMatchGlossary(datum)
    extractmatchAttacking(datum)

def extractmatchAttacking(datum):
    ## matchAttackinng == 19
    print("--extractmatchAttacking--\n")
    num = 21
    data = datum[list(datum.keys())[num]]
    keySet = list(data.keys())
    print(keySet)
    print(len(data['col']))
    print(data['col'][0][0]['data'])
    print("\n")

    for item in data['col'][1][0]['data']:
        print(item.keys())
        print(item.values())
        print("\n")



def extractMatchGlossary(datum):
    ## MatchGlossary == 22
    num  = 22
    data = datum[list(datum.keys())[num]]
    keySet = list(datum.keys())
    '''
    print(len(datum[keySet[num]]))
    print(datum[keySet[num]]['col'][0])
    print("\n")
    print(datum[keySet[num]]['col'][1])
    print("\n\n\n")
    '''
    def iterateList(listee):

        for value in listee:
            print(value['data'].keys())
            print(value['data'].values())
            print("\n")

    iterateList(datum[keySet[num]]['col'][0])
    print("\n")
    iterateList(datum[keySet[num]]['col'][1])

    '''
    for k, v in datum[keySet[num]]['col']:
        print(k , v)
        print("\n")
    '''


def extractMatchDiscipline(datum):
    ## matchDiscipline == 23
    ## ignore everything but the values found in 'col'
    ## datum['matchDiscipline']['col'][0]
    ## content to be found at datum['matchDiscipline']['col'][1][0]['data']
    num  = 23
    data = datum[list(datum.keys())[num]]
    data =  data['col']

    #print(datum['matchDiscipline']['col'][0])
    #print("\n")
    #print(datum['matchDiscipline']['col'][1])

    print(10*"^")
    for dict1 in datum['matchDiscipline']['col'][1][0]['data']:
        print(dict1.keys())
        print(dict1.values())
        print("\n")


    print(datum['matchDiscipline']['col'][0][0]['data'].keys())
    print(datum['matchDiscipline']['col'][0][0]['data'].values())


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
    #print(d_0)
    print(50*"=")
    print("\n")


    ## module drills into text found in the first list and retrieves
    ## number of tries in the game
    #trydata = type(k['data'][0])
#    print(type(trydata))
    ## key is made up of type/data - we are interested in data
    k = list(d_0)
    trydata = k[0]['data']
    #print(len(trydata))
    for event in trydata:
        #print(event['text'])
        print(event.values())

    print("\n")
    print(10*"== one =")

    d_1 = list(d[1])
    #targetData = d_1[0]['data']

    print(d_1[0]['data'])

    for item in d_1[1]['data']:
        print(item)

    #print(datum.keys())
    #print(datum['title'])
    #print("\n***\n")

    return d


def examineMatchHeadtoHead(datum):
    # headToHead found in 31
    # datum = stats['gamePackage'] --> directly drill into target area in match
    num = 31
#    print(datum[list(datum.keys())[num]][0])
    dataDict = datum[list(datum.keys())[num]][0]
    #print(datum[list(datum.keys())[num]])
    print(50*"=-=-")
    ## Title of area of interest
    print(list(datum.keys())[num] )
    ## int location of variable
    print(num)

    ## look at the keys of interest
    print(dataDict.keys())
    ## keys are team and event
    # team == 6  :: type dict
    # events == 5 :: type List
    #print(type(dataDict['team']))
    print(10*"-")
    #print(len(dataDict['events']))
    # [1, 3 ]

    ## not much going on in 'events'
        # 3 == date/time
        # 4 == final score
        # 14 == name o team

    values = list(dataDict['team'].keys())
    for value in dataDict['events']:
        print(type(value))
        print(value.keys())
        print(10*"--")
        print(value.values())

def extractMethodInstances(stats):
    ## all data exists in 'gamePackage'
    ## takes in stats from getGameMetaData
    # ----> drills into just the window area of the html page
    # return matchEvents
    datum =  stats['gamePackage']
    matchStats = extractAllSuperMethod(datum)
    ## method takes in matchStats and returns a friendly representation
    sortedData = cleanMatchStats(matchStats)


def cleanMatchStats(matchStats):
    print("---cleanMatchStats---")
    Data = []
    ## first pass take out all the set ones
    for item in matchStats:
        if len(item) == 3:
            Data.append(item)
        else:
            ## first exception array of 4 error point removed
            if len(item) != 5:
                item = removeFirstEntry(item, 1 , len(item))
                Data.append(item)
            else:
            ## second exception "Possession" has dublicate values
                if item['text'] == "Possession":
                    item = removeFirstEntry(item, 2 , len(item))
                    Data.append(item)
                else:
                ## third exception when values are lumped
                    Data.extend(splitDictInTwo(item))
    return Data

def splitDictInTwo(item):
    print("---splitDictInTwo---")
    itemA = removeFirstEntry(item, 0 , 2)
    itemA['text'] = item['text'] + "_home"
    itemB = removeFirstEntry(item, 2 , len(item))
    itemB['text'] = item['text'] + "_away"
    return [itemA, itemB]

def removeFirstEntry(item, start, stop):
    print("---removeFirstEntry---")
    keys = list(item.keys())[start:stop]
    values = list(item.values())[start:stop]
    dictionary = dict(zip(keys, values))
    return dictionary

def extractAllSuperMethod(datum1):
    print("---extractAllSuperMethod---")
    # no1 matchEvents
    #datum = datum1
    sect = "matchEvents"
    datum = datum1[sect]['col']
    allDatum = []

    # box 1
    allDatum = retrieveListDictValues(datum[0][0]['data'], allDatum)
    # box 2 - header
    allDatum = retrieveListDictValues(datum[1][0]['data'], allDatum)
    # box 2 - content
    allDatum = retrieveListDictValues(datum[1][1]['data'], allDatum)
    # box 3 - extractmatchAttacking

    #num = 21
    sect = 'matchAttacking'
    datum = datum1[sect]['col']
    allDatum = retrieveListDictValues(datum[0][0]['data'], allDatum)
    # box 2 - header
    allDatum = retrieveListDictValues(datum[1][0]['data'], allDatum)
    # box 2 - content
    #allDatum = retrieveListDictValues(datum[1][1]['data'], allDatum)

    #num = 22
    sect = "matchDefending"
    datum = datum1[sect]['col']

    # first box 1
    allDatum = retrieveListDictValues(datum[0][0]['data'], allDatum)
    #frst box 2
    allDatum = retrieveListDictValues(datum[0][1]['data'], allDatum)
    # box 2 - header
    allDatum = retrieveListDictValues(datum[1][0]['data'], allDatum)
    # box 5 -

    #num = 23
    sect = "matchDiscipline"
    datum = datum1[sect]['col']

    # first box 1
    allDatum = retrieveListDictValues(datum[0][0]['data'], allDatum)
    #frst box 2
    allDatum = retrieveListDictValues(datum[1][0]['data'], allDatum)

    return allDatum
    '''
    print(len(allDatum))
    for item in allDatum:
        print(type(item))
        print(item)
    '''

def retrieveListDictValues(datum, allDatum):
    #print(len(datum))
    #print(datum)
    if returnDict(datum):
        allDatum.extend(datum)
    else:
        allDatum.append(datum)

    return allDatum

def returnDict(inp):
    if isinstance(inp, list):
        return True

    return False

#    print(type(datum['col'][0][0]))
#    print(len(datum['col'][0][0]['data']))

#    valueList = []
#    for value in datum['col'][0][0]['data']:
#        valueList.append(list(value.values()))

#    return (list(datum['col'][0][0]['data'][0].keys()) , valueList)

    #return(list(value.keys()), list(value.values())

    '''
    val = "home"
    #print(val)

    #print((datum[list(datum.keys())[num]])[val])
    #print(len(datum[list(datum.keys())[num]][val]))
    datumKeys = list(datum.keys())
    #print(len(datumKeys))
#    print(datum[datumKeys[num]][val])
    title = datumKeys[num]
    keySet = list(datum[title].keys())
    print(keySet)

    print("-=-=-=-")
    print(keySet[0])
    print(datum[title][keySet[0]])
    print(datum[title][keySet[0]].keys())
    print("8-=-=-=-8")
    print(keySet[1])
    print(datum[title][keySet[1]])
    #print(datum)
    '''



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
