from scrapeData import createFileList , extractMatchDateLeague, extractPlayerDeets , extractMethodInstances, getMetaData , extractAllPlayers , getGameMetaData
#from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable
from mainDbCreation import  createUniqueIdentifierDict,  analyseOneGame, processingDates ,readDBPandas, deleteTable, insertMatchData, readDBMatchMeta, createMetaMatchTable,  sanitiseMetaList, createPrimaryKey, extractDBcontent, returnColumnHeaders ,  extractDaysPlayerMatchDetails, deleteTable, createTable , insertPlayerData , readDB , readingFilesList
import matplotlib.pyplot as plt
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


## create loop , cantains variable that cvan be extended to go back through games
#createFileList()
#fl = readingFilesList()
#print(len(fl))
#analyseOneGame("http://www.espn.co.uk/rugby/matchstats?gameId=293566&league=271937")
mainGo = False
if mainGo:
    # teamList for debugging purposes
    teamList = []
    for file in fl:
        print(file)
        print("\nstats\n")
        stats = getMetaData(file)

        print("\nmatchId\n")
        matchId = createPrimaryKey(file)

        #print(fl[0])
        ### temporarily comment code , contains work on extracting match data for first two message boxes
        #getGameMetaData(stats)
        ## takes in the htmnl for any given map
        # method extracts league and date
        metaData = analyseOneGame(stats)
        print(10*"8")
        print(metaData)
        #print("------- matchID\n\n\n\n")
        #print(metaData)
        # extracts main match points
        matchValues = extractMethodInstances(stats)
        # add date/league to match data
        sanitisedList = sanitiseMetaList(matchValues[2:])
        sanitisedList.extend(matchValues[:2])
        print(sanitisedList.extend(metaData))
        #sanitisedList.extend(metaData)
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
        ## needs to be uncommented if you intend to add to the db
        teamb = insertMatchData(colheads, listAway)
        team = insertMatchData(colheads, listHome)


        #teamList.append(team[34])
        #teamList.append(teamb[34])
'''
        print(10*"--")
    for team in teamList:
        print(team)
'''

####### ->>> datatable allows duplicates, remove.

deletDB = False
if (deletDB):
    try :
        deleteTable("MATCHES")
    except:
        print("able does not exits")




##- create a deletetable for teams
## to create the table
createTable = False
if createTable:
    #primaryKey = createPrimaryKey(fl[0])
    #print(primaryKey)
    ## extract meta match data
    #df = pd.DataFrame()
    createMetaMatchTable(df)
    print()
#print(df.shape)
#print(df)
## read the db
#print(3*" \n ")
def printingLeagueTable():
    print("--------- datatable output -------------")
    data = readDBMatchMeta(show = False)
    cols = returnColumnHeaders()
    df = pd.DataFrame(columns = cols,data =  data)
    df = processingDates(df)
    ## converting string datetime to datetime date.
    df['order'] = df.date.dt.week
    #print(df.head())
    def sanitiseData(df):
        date = df.date
        df.drop(['date'], axis=1, inplace = True)
        for col in df.columns:
            print(col)
            if col == "teams" or col == "league" or col == "ID":

                df[col] = df[col].astype('category')
                #print(df.teams)
                cat_columns = df.select_dtypes(['category']).columns
                #print(cat_columns)
                temp = df[cat_columns].apply(lambda x: x.cat.codes)
                #print(temp)
                df[col] = temp[col]
                ## todo retrieve list of teams
            df[col] = df[col].astype(float)
        df.drop(['ID'], axis=1, inplace = True)
        df.drop(['league'], axis=1, inplace = True)
        df.drop(['teams'], axis=1, inplace = True)

        return df


    def plotting():
        df = df.sort_values('date', ascending = "True")
        df.groupby(df['date'])
        plt.plot(df['order'], df['score'])
        plt.xticks(rotation='vertical')
        plt.show()
        print(df.date)

    df_sanitised = sanitiseData(df)

    won = df_sanitised.groupby(['winLoss']).get_group(1)
    loss = df_sanitised.groupby(['winLoss']).get_group(0)
    x = list(loss.score)
    y = list(won.score)
    plt.plot(x, y )

#readDBPandas()



########################################################
################
## Obtaining alternaitve league data
##################
#######################################################
# championsCup 2018
# starts http://www.espn.co.uk/rugby/report?gameId=291704&league=271937
# ends  http://www.espn.co.uk/rugby/report?gameId=292810&league=271937
##############################################

#################################
### 1. obtain league data
#createFileList(291704, 292810)

## scratch that -- obtaining six nations data
# 2018 http://www.espn.co.uk/rugby/matchstats?gameId=291703&league=180659
# 2017 http://www.espn.co.uk/rugby/matchstats?gameId=290916&league=180659
# 2016 http://www.espn.co.uk/rugby/matchstats?gameId=254989&league=180659
# 2015 http://www.espn.co.uk/rugby/matchstats?gameId=180687&league=180659
# 2014 http://www.espn.co.uk/rugby/matchstats?gameId=180666&league=180659
# 2013 http://www.espn.co.uk/rugby/matchstats?gameId=133787&league=180659
# 2012 http://www.espn.co.uk/rugby/matchstats?gameId=133769&league=180659
# 2011 http://www.espn.co.uk/rugby/matchstats?gameId=114130&league=180659
# 2010 http://www.espn.co.uk/rugby/playerstats?gameId=94951&league=180659
#createFileList(94931, 94971, leagueID =  180659, compName= "sixNations")

##### 2. iterate over the list and pull out all of the metaMatchDetails
leagueName = "sixNations"
fl = readingFilesList(leagueName)

sixNationsRun = False
if(sixNationsRun):
    for file in fl:
        #### 3. retrieve the stats for one game to use for table creation ####
        stats = getMetaData(file)
        ## metaData is few extra tidbits
        metaData = analyseOneGame(stats)
        ## grab the main chunk of stuff
        matchValues = extractMethodInstances(stats)
        # clean your data skipping first pesky ones
        sanitisedList = sanitiseMetaList(matchValues[2:])
        sanitisedList.extend(matchValues[:2])
        # combine with previous tidbits
        sanitisedList.extend(metaData)
        # create unique identifer
        dict = createUniqueIdentifierDict(file)
        sanitisedList.append(dict)
        # break match into two teams
        df = pd.DataFrame(sanitisedList)
        listAway = list(df['awayValue'])
        listHome = list(df['homeValue'])
        colheads = list(df['text'])

        # create table
        createNewTable = True
        if createNewTable:
            try:
                createMetaMatchTable(df, "sixNations")
            except:
                print("table already exists")
                createNewTable = False

        # insert into Table
        insertToTable = True
        if insertToTable:
            teamb = insertMatchData(colheads, listAway, "sixNations")
            team = insertMatchData(colheads, listHome, "sixNations")

        deletDB = False
        if (deletDB):
            try :
                deleteTable("sixNations")
            except:
                print("able does not exits")
# retrieve data
table = readDB("sixNations", False)

columns = returnColumnHeaders(leagueName)
print(columns)

df = pd.DataFrame(table, columns = columns)

'''
['score', 'Tries', 'Conversion Goals', 'Penalty Goals', 'Kick Percent Success',
'Metres Run', 'Kicks From Hand', 'Passes', 'Runs', 'Possession', '2H_Possession',
 '1H_Possession', '2H_Territory', '1H_Territory', 'Clean Breaks', 'Defenders Beaten',
 'Offload', 'Rucks won', 'Rucks lossed', 'Mauls won', 'Mauls lossed', 'Turnovers Conceded',
 'Scrums loss', 'Scrums won', 'Lineouts loss', 'Lineouts won', 'Tackles loss', 'Tackles won',
 'Penalties loss', 'Penalties won', 'Red Cards', 'Yellow Cards', 'Total Free Kicks Conceded',
 'winLoss', 'teams', 'league', 'date', 'ID']
'''
print(df['Tries'])
