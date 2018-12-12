from scrapeData import extractPlayerDeets , getMetaData
#from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable
from mainDbCreation import deleteTable, createTable , insertPlayerData , readDB
stats = getMetaData()

num = 3
HA = "away"
#dynamicTableCreation()
#createTable(stats)
name, playerValues, colheads = extractPlayerDeets(stats, num, HA)

## runs table , should only be run once
# - createTable(colheads)

# inputs the extracted list
#insertPlayerData(colheads, playerValues)
readDB()

#inputValue()
# - readDB()
# - deleteTable()
#readDB()
