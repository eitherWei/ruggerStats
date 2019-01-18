from scrapeData import createFileList , extractMatchDateLeague, extractPlayerDeets , extractMethodInstances, getMetaData , extractAllPlayers , getGameMetaData
#from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable
from mainDbCreation import deleteTable, insertMatchData, readDBMatchMeta, createMetaMatchTable,  sanitiseMetaList, createPrimaryKey, extractDBcontent, returnColumnHeaders ,  extractDaysPlayerMatchDetails, deleteTable, createTable , insertPlayerData , readDB , readingFilesList
'''
#deleteTable()

fl = readingFilesList()
print(fl)
stats = getMetaData(fl[0])


#--------------------name, playerValues, colheads = extractPlayerDeets(stats, num, HA)
#--------------------deleteTable()

# extracts all of the deets on all of the players for one side
playerList , colheads = extractAllPlayers(stats, 'home')

## runs table , should only be run once
createTable(colheads)

# inputs the extracted list
#def insertListToDataBase(playerList, colheads):
#    for playerValues in playerList:
#        insertPlayerData(colheads, playerValues)

#insertListToDataBase(playerList, colheads)
#readDB()
'''
'''
# use the old column headers to inform the new ones
colheads  = returnColumnHeaders()
print(len(colheads))
#print(colheads)
# delete previous version of the table
#deleteTable()
## runs table , should only be run once
#createTable(colheads)
#  does all of the heavy lifting , needs appropriate table with correct columns
#extractDaysPlayerMatchDetails()

#print(10*"-")
#print(colheads)
df = extractDBcontent()
print(df.head())

df.to_csv('data/processedTable.csv')
'''


import pandas as pd


# extract metadata for last weekends match
# 1 get files

#createFileList()
fl = readingFilesList()

mainGo = True
if mainGo:
    for file in fl:
        print(file)
        stats = getMetaData(file)
        matchId = createPrimaryKey(file)
        #print(fl[0])
        ### temporarily comment code , contains work on extracting match data for first two message boxes
        #getGameMetaData(stats)
        ## takes in the htmnl for any given map
        # method extracts league and date
        metaData = extractMatchDateLeague(stats)
        # extracts main match points
        matchValues = extractMethodInstances(stats)
        # add date/league to match data
        sanitisedList = sanitiseMetaList(matchValues[2:])
        sanitisedList.extend(matchValues[:2])
        sanitisedList.extend(metaData)
        df = pd.DataFrame(sanitisedList)
        # put a list of team stuff into the data base
        listAway = list(df['awayValue'])
        listAway.append(matchId+ "a")
        listHome = list(df['homeValue'])
        listHome.append(matchId + "h")
        colheads = list(df['text'])
        colheads.append("ID")
        ## append date and time
        #colheads.append("league")
        #colheads.append("date")
        print("--------- list output ----------------")
        #print(liste)
        #insertMatchData(colheads, listAway)
        #insertMatchData(colheads, listHome)


####### ->>> datatable allows duplicates, remove.

deletDB = False
if (deletDB):
    try :
        deleteTable("MATCHES")
    except:
        print("able does not exits")

## to create the table
createTable = False
if createTable:
    #primaryKey = createPrimaryKey(fl[0])
    #print(primaryKey)
    ## extract meta match data
    createMetaMatchTable(df)
    print()



##- create a deletetable for teams

#print(df.shape)
#print(df)
## read the db
print(3*" \n ")
print("--------- datatable output -------------")
readDBMatchMeta(show = True)
