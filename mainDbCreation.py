import sqlite3 as sq
# import regex to sanitise list inputs
import re

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

def readDB():
    db.row_factory = sq.Row
    # create an execute statement
    insertStatement = ''' SELECT * FROM users1 '''
    # execute the action
    cursor.execute(insertStatement)
    # extract the table items
    data = cursor.fetchall()

    print(len(data))
    print(10*"-")
    for d in data:
        print(d)


    return data


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
