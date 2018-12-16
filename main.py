from scrapeData import extractPlayerDeets , getMetaData , extractAllPlayers
#from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable
from mainDbCreation import  extractDBcontent, returnColumnHeaders ,  extractDaysPlayerMatchDetails, deleteTable, createTable , insertPlayerData , readDB , readingFilesList


'''
fl = readingFilesList()
print(fl)
stats = getMetaData(fl[0])

#num = 3
#HA = "away"
#dynamicTableCreation()

#--------------------extractPlayerDeets(stats, num, HA)
#--------------------name, playerValues, colheads = extractPlayerDeets(stats, num, HA)
#--------------------deleteTable()

# extracts all of the deets on all of the players for one side
playerList , colheads = extractAllPlayers(stats, 'home')

## runs table , should only be run once
#eateTable(colheads)

# inputs the extracted list
#def insertListToDataBase(playerList, colheads):
#    for playerValues in playerList:
#        insertPlayerData(colheads, playerValues)

#insertListToDataBase(playerList, colheads)
#readDB()
'''

#inputValue()
# - readDB()
# - deleteTable()



#print(10*"-")
#print(colheads)
df = extractDBcontent()




#extractDaysPlayerMatchDetails()
