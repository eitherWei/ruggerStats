import sqlite3 as sq

db = sq.connect('data/mydb')
cursor = db.cursor()

rowNumbers = 32

def createTable(headers):
	#headers = 	 [ "name" ,  "phone",  "email" , "password" ]

	try:


		## connects to the database
		#db = sq.connect('data/mydb')
		# get a cursor object
		#cursor = db.cursor()
		# check if the table exists

		#dropTableStatement = "DROP TABLE users1"

		#cursor.execute(dropTableStatement)

		#db.commit()
		#print("table deleted")
	
		print(headers[:rowNumbers])
		insertStatement = "CREATE TABLE IF NOT EXISTS  users1 %s " % (tuple(headers[:rowNumbers]),)
		#insertStatement = insertStatement + " VALUES %s" % (tuple(headers),)

		#cursor.execute('''CREATE TABLE IF NOT EXISTS
		#					users(id INTEGER PRIMARY KEY , name TEXT, phone TEXT, email TEXT, password TEXT)''')

		cursor.execute(insertStatement)

		db.commit()
		print("table created")

	except Exception as e:
		db.rollback()
		print(e)
		raise e

	#finally:
		#db.close()

def inputValue():
	name = "andreas"
	phone = "123"
	email = "here@here.com"
	password = "123"

	playerValues = ["one", "two", "three", "four"]
	try:
		## connects to the database
		db = sq.connect('data/mydb')
		with db:
			#db.execute(''' INSERT INTO users(name, phone, email, password)
			#VALUES(?,?,?,?)''', (name, phone, email,password))
			db.execute(''' INSERT INTO users4(name, phone, email, password)
			VALUES(?,?,?,?)''', tuple(playerValues))
			print("input proceseed")
	except sq.IntegrityError:
		print("record already exists")
	finally:
		db.close()


def dynamicTableCreation():
	global db
	tableName = "stat1"
	data_list = ['id', 'url', 'name', 'number', 'position', 'captain', 'subbed', 'homeAway', 'subToolTip', 'eventTimes', 'onPitch', 'wasActive', 'tries', 'tryassists', 'points',
	 'kicks', 'passes', 'runs', 'metres', 'cleanbreaks', 'defendersbeaten', 'offload',
	 'lineoutwonsteal', 'turnoversconceded', 'tackles', 'missedtackles', 'lineoutswon',
	 'penaltiesconceded', 'yellowcards', 'redcards', 'penalties', 'penaltygoals', 'conversiongoals', 'dropgoalsconverted']
	db = sq.connect("data/mydb")
	commie = "CREATE TABLE IF NOT EXISTS users2("
	for data in data_list:
		commie = commie + data + " , " + "TEXT "
	commie = commie + ")"
	#print(commie)
	db.execute(commie)

	cursor = db.cursor()
	cursor.execute("PRAGMA table_info(users2)")
	heads = list(cursor.fetchall())
	print(heads)
	#db.execute("CREATE TABLE IF NOT EXISTS " + tableName +" VALUES(" + ('?,' * len(data_list))[:-1] + ")", data_list)

def dynamicTableCreation2():
	createStatment = "CREATE TABLE IF NOT EXISTS users3"
#dynamicTableCreation()

def sanitiseList(liste):
	strList = []
	for item in liste:
		print(type(item))
		if type(item) is list:
			#item = item.replace('""', " ")
			item = item[0]
		strList.append(str(item))

	return strList
def insertPlayerData(colheads, list):
	#headers = 	 [ "name" ,  "phone",  "email" , "password" ]
	print(colheads[:rowNumbers])
	print(list[:rowNumbers])
	print(10*"^")

	## sanitise the list
	list = sanitiseList(list)

	insertStatement = "INSERT INTO users1 %s " % (tuple(colheads[:rowNumbers]),)
	insertStatement = insertStatement + " VALUES %s " % (tuple(list[:rowNumbers]),)
	#db.execute(''' INSERT INTO users(name, phone, email, password)
	#VALUES(?,?,?,?)''', tuple(list))
	#print(insertStatement)
	cursor.execute(insertStatement)
	db.commit()
	#db.close()


def readDB():
	print("read table")
	db = sq.connect("data/mydb")
	db.row_factory = sq.Row
	cursor = db.cursor()
	cursor.execute(''' SELECT * FROM users1 ''')
	data = cursor.fetchall()
	print(type(data))
	'''
	for row in data:
		print(row.keys())
		for r  in row:
			print(r)
		#print(row.values())
		#print('{0} : {1}, {2}'.format(row['id'], row['name'], row['number']))
	#db.close()
	'''
	print(len(data))
