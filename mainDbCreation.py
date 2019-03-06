import sqlite3 as sq
from scrapeData import extractPlayerDeets , getMetaData , extractAllPlayers , extractMatchDateLeague , getGameMetaData
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

def createMetaMatchTable(headers, tableName):
    #print(headers)
    def createTable(headers, tableName):
        print(headers.shape)
        print(10*" %% ")
        print(headers.columns)
        headers = list(headers.text)
        print(headers)
        insertStatement = "CREATE TABLE IF NOT EXISTS " + tableName + " %s " % (tuple(headers), )
    #    insertStatement = "CREATE TABLE MATCHES (ID INT PRIMARY KEY);  "
        cursor.execute(insertStatement)
        db.commit()
        cursor.execute(insertStatement)
        try:
            cursor.execute("alter table" + tableName + "add column ID ;")
            db.commit()
        except:
            print("althering comment ")

        print("table commited ")

    createTable(headers, tableName)


def readDBMatchMeta(show = False):
    db.row_factory = sq.Row
    # create a select statement
    insertStatement = ''' SELECT * FROM MATCHES '''
    # execute the action
    cursor.execute(insertStatement)
    # extract the table items
    data = cursor.fetchall()

    if(show):
        for d in data:
            print(d)
    print(10*"-")
    print(len(data))
    print(10*"-")

    return data

def analyseOneGame(stats):
    #print(url)
    ## extract the stats
#    metaData = getGameMetaData(stats)
    datum = stats['gamePackage']["gameStrip"]
    #print(len(datum))
    #print(datum.keys())
    #print(datum['isoDate'])
    #print(datum['header'])

    return [{"homeValue" : datum['header'], "awayValue" : datum['header'] , "text" : "league" } , {"homeValue" : datum['isoDate'], "awayValue" : datum['isoDate'] , "text" : "date" }]

    #print(10*"8")
    #print(metaData)

def insertMatchData(colheads, liste, tableHead):
    insertStatement = "INSERT INTO " +  tableHead +  " %s " % (tuple(colheads),)
    # create variable string
    insertStatement = insertStatement + " VALUES %s " % (tuple(liste), )
    # create execute action
    cursor.execute(insertStatement)
    # conmit the action
    db.commit()

    return liste


def sanitiseMetaList(List):
    allData = []
    headers = ['homeValue', 'awayValue', 'text']
    for item in List:
        title = list(item.values())[-1]
        lista = convertToInt(list(item.values()))
        lista.append(title)
        lista = dict(zip(headers, lista))
        allData.append(lista)

    return allData




def convertToInt(list):
    tempList = []
    for item in list[:-1]:
        #print(item)
        try:
            item = re.sub("\D", "", item)
        except:
            item = item
        #print(int(item))
        tempList.append(int(item))
    return tempList

# method takes the input url and generates a unique ID
def createPrimaryKey(str):
    print(str)
    # remove the proceeding url
    str = str.split("?")
    str = str[1]
    str = str.split("&")
    # separate into gameID and LeagueID
    ## insert incrementor here
    key = ""
    for value in str:
        st = value.split("=")
        key += st[1]
    return(key)


def readDB( tableName , show = False):
    #names = [description[0] for description in cursor.description]
    #print(names)
    db.row_factory = sq.Row
    # create an execute statement
    insertStatement = ''' SELECT * FROM ''' + tableName
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

def readDBPandas(tableName):
    # Create your connection.
    cnx = sq.connect('mydb.db')

    df = pd.read_sql_query("SELECT * FROM " +  tableName , cnx)
    print(df.head())


def returnColumnHeaders(tableName):
    colheads = cursor.execute("PRAGMA table_info(" + tableName + ")")
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

def readingFilesList(compName = "championsCup.txt"):
    print("reading files found in " + compName)
    file = open(compName)
    fileList = []
    for line in file:
        fileList.append(line.rstrip('\n'))

    print(str(len(fileList)) + " number of files found")
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




def deleteTable(tb):
    try:
        # create drop statement
        dropTableStatement = "DROP TABLE " + tb
        # execute the action
        cursor.execute(dropTableStatement)
        # commit to db
        db.commit()
        print("table deleted")
    except:
        print("error deleting table")
        # remove grit
        db.rollback()


def processingDates(df):
    #print(df.head())
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    #print(df['date'].dt.date)
    df['date'] = pd.to_datetime(df.date)
    ## returns  numberical represent of the week .. perfect !
    #print(df.date.dt.week)
    df = df.sort_values('date', ascending = "True")
    return df

def createUniqueIdentifierDict(file):
    matchId = createPrimaryKey(file)
    ## create idDict
    dict = {"homeValue" : matchId+ "h", "awayValue": matchId+ "a", "text" : "ID" }
    return dict
