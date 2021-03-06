import sqlite3 as sq
from scrapeData import extractPlayerDeets , getMetaData , extractAllPlayers
# import regex to sanitise list inputs
import re
import pandas as pd

db  = sq.connect('data/mydb')
cursor = db.cursor()
'''
    matchTable
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    uniqueId #    match_stats            # player_stats
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    int      #    list[match details]    # list[playerDict]

    # list[playerDict] == a dictionary for eachPlayer
    # uniqueMatchId to be used as primary key in player list
'''
def readDB(show = False):
    #names = [description[0] for description in cursor.description]
    #print(names)
    db.row_factory = sq.Row
    # create an execute statement
    insertStatement = ''' SELECT * FROM users1 '''
    # execute the action
    cursor.execute(insertStatement)
    # extract the table items
    data = cursor.fetchall()

    # uncomment to get a database readout
    if(show):
        for d in data:
            print(d)
    print(10*"-")
    print(len(data))
    print(10*"-")


    return data

def returnColumnHeaders():
    colheads = cursor.execute("PRAGMA table_info(users1)")
    #print(type(colheads))
    cols = []
    for d in colheads:
        #print(d)
        cols.append(d[1])

    return cols

def sanitise_list(colheads, liste):
    # create list to hold cleaned values
    sanitisedList = []
    for data in liste:
        # check if it is an instance of a list
        if isinstance(data, list):
            # if list take the first instance
            data = data[0]
            data = re.sub("\D", "", data)
        # add string item to cleaned list
        sanitisedList.append(str(data))
    # return cleaned list
    return sanitisedList

def insertPlayerData(colheads, liste):
    # clean input of varying forms int/boolean/list/string
    inputList = sanitise_list(colheads, liste)
    ## create input statement
    # create header string
    insertStatement = "INSERT INTO users1 %s " % (tuple(colheads),)
    # create variable string
    insertStatement = insertStatement + " VALUES  %s " % (tuple(inputList),)
    # execute the action
    cursor.execute(insertStatement)
    # commit the execution
    db.commit()

def deleteTable():
    try:
        # create drop statement
        dropTableStatement = "DROP TABLE users1"
        # execute the action
        cursor.execute(dropTableStatement)
        # commit the comment
        db.commit()
        print("table deleted")
    except:
        print("error deleting db")
        # remove any grit
        db.rollback()

def createTable(headers):
    print(headers)
    # create insert table
    insertStatement = "CREATE TABLE IF NOT EXISTS USERS1 %s " % (tuple(headers), )
    # execute the action
    cursor.execute(insertStatement)
    # commit the comment
    db.commit()
    print("table commited")

    # create a unique key so that no dublicate data  can be added
    # method needs to be update to return a concat key of game and player to ensure no dublicate data
    #sql = ("CREATE INDEX id ON users1 (id);")
    #cursor.execute(sql)
    #db.commit()

    # create an additional column that keeps score
    sql = "ALTER TABLE users1 ADD COLUMN finalScore TEXT"
    cursor.execute(sql)
    db.commit()

def readingFilesList():
    file = open("gamesList")
    fileList = []
    for line in file:
        fileList.append(line.rstrip('\n'))

    return fileList

# inputs the extracted list
def insertListToDataBase(playerList, colheads):
    for playerValues in playerList:
        insertPlayerData(colheads, playerValues)



def extractDaysPlayerMatchDetails():
    # get the stats list to where all of the games are stored
    fl = readingFilesList()
    # create a list to get home and away teams
    teams = ['home', 'away']

    for match in fl:
        # get the html page
        stats = getMetaData(match)
        #extract all match player details
        for team in teams:
            playerList , colheads = extractAllPlayers(stats, team)
            # iterate over the playerList then put in DB
            print("length of colheads being inserted")
            print(len(colheads))
            print(colheads)
            insertListToDataBase(playerList, colheads)
            # read the db to show progressive growth
            readDB()

def extractDBcontent():
    data = readDB()
    colheads  = returnColumnHeaders()

    df = pd.DataFrame( columns  = colheads , index = [i for i in range(len(data))])
    for i in range(len(data)):
        df.loc[i] = data[i]
    #print(df.head())
    wantedColheads = [ 'position', 'homeAway', 'tries', 'tryassists', 'points', 'kicks', 'passes', 'runs', 'metres', 'cleanbreaks', 'defendersbeaten', 'offload', 'lineoutwonsteal', 'turnoversconceded', 'tackles', 'missedtackles', 'lineoutswon', 'penaltiesconceded', 'yellowcards', 'redcards', 'penalties', 'penaltygoals', 'conversiongoals', 'dropgoalsconverted', 'finalScore']
    new = df.filter(wantedColheads, axis=1)

    new = convertDFtoInts(new)
#    print(new.head())
#    print(new['finalScore'])
    return new

def convertDFtoInts(df):
    print(df.head())
    df[df.columns[0]] = df[df.columns[0]].astype('category').cat.codes
    df = df.apply(pd.to_numeric, errors='ignore')

    df['homeAway'].replace(to_replace = ["home", "away"], value = [1,0], inplace = True)
    ## casting win loss to a varaibale
    # remove punctuation
    df.finalScore = df.finalScore.apply(lambda x: x.split("-"))
    # cast to int
    winLoss = []
    for index , row in df.iterrows():
        # cast to int
        temp = [int(i) for i in row['finalScore']]
        # check if home team and return final score in their favour
        if(row['homeAway'] == 1 and temp[0] > temp[1]):
            winLoss.append(1)
        else:
            winLoss.append(0)
    df.finalScore = winLoss

    return df
