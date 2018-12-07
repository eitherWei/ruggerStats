from scrapeData import extractPlayerDeets , getMetaData
from dbCreation import insertPlayerData , inputValue , readDB , dynamicTableCreation , createTable

stats = getMetaData()

num = 3
HA = "away"
#dynamicTableCreation()
#createTable(stats)
name, playerValues, colheads = extractPlayerDeets(stats, num, HA)
createTable(colheads )
#print(len(playerValues))
#playerValues = ["one", "two", "three", "four"]
insertPlayerData(colheads, playerValues)

#inputValue()
readDB()
