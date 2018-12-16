from scrapeData import extractPlayerDeets , getMetaData , extractAllPlayers
#from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable
from mainDbCreation import  extractDBcontent, returnColumnHeaders ,  extractDaysPlayerMatchDetails, deleteTable, createTable , insertPlayerData , readDB , readingFilesList
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
