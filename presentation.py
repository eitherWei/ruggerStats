
from mainDbCreation import readDB , returnColumnHeaders  , processingDates
import pandas as pd

leagueName = "sixNations"
# retrieve data
table = readDB("sixNations", False)

columns = returnColumnHeaders(leagueName)
print(columns)

df = pd.DataFrame(table, columns = columns)


#df = processingDates(df)
#df['order'] = df.date.dt.week
#print(df['date'])
#print(df['order'])

timeStamp = list(df['date'])
tries =  list(df['Tries'])

t1 = pd.DataFrame( list(zip(timeStamp, tries)), columns = ["time", "score"])

t2 = pd.DataFrame(tries, index = timeStamp)
#print(t2.head())
t2.index = pd.to_datetime(t2.index)
#print(t2.head())

import matplotlib.pyplot as plt

#t2.plot()
#plt.show()

df['date'] = pd.to_datetime(df['date'])
df['year'], df['month'], df['week'] = df['date'].dt.year, df['date'].dt.month , df['date'].dt.week
print(df.head())


def extractFirstYear(df, year):
    crit1 = df[df.year == year]
    return crit1

def extractFirstWeek(df, week):
    crit1 = df[df.week == week]
    return crit1


tryArray = []
for i in range(2010, 2019):
    print(i)
    yearChart = extractFirstYear(df , i)
    #print(yearChart)
    weekChart = extractFirstWeek(yearChart , 5)
    #print(weekChart)
    openingTryCount = weekChart.Tries.sum()
    tryArray.append(openingTryCount)

print(tryArray)





#x = t18.week.value_counts()
#print(x)



#print(t1)
#print(list(df['Tries']))
['score', 'Tries', 'Conversion Goals', 'Penalty Goals', 'Kick Percent Success',
'Metres Run', 'Kicks From Hand', 'Passes', 'Runs', 'Possession', '2H_Possession',
 '1H_Possession', '2H_Territory', '1H_Territory', 'Clean Breaks', 'Defenders Beaten',
 'Offload', 'Rucks won', 'Rucks lossed', 'Mauls won', 'Mauls lossed', 'Turnovers Conceded',
 'Scrums loss', 'Scrums won', 'Lineouts loss', 'Lineouts won', 'Tackles loss', 'Tackles won',
 'Penalties loss', 'Penalties won', 'Red Cards', 'Yellow Cards', 'Total Free Kicks Conceded',
 'winLoss', 'teams', 'league', 'date', 'ID']
