import sqlite3 as sq


def createTable():
	try: 
		## connects to the database
		db = sq.connect('data/mydb')
		# get a cursor object
		cursor = db.cursor()
		# check if the table exists 
		cursor.execute('''CREATE TABLE IF NOT EXISTS
							users(id 	INTEGER PRIMARY KEY , name TEXT, 	phone TEXT, email TEXT, password TEXT)''')
		
		db.commit()
		
	except Exception as e:
		db.rollback()
		print(e)
		raise e 

	finally:
		db.close()

def inputValue():		
	name = "andreas"
	phone = "123"
	email = "here@here.com"
	password = "123"

	try:
		## connects to the database
		db = sq.connect('data/mydb')
		with db:
			db.execute(''' INSERT INTO users(name, phone, email, password)
			VALUES(?,?,?,?)''', (name, phone, email,password))
			print("input proceseed")
	except sq.IntegrityError:
		print("record already exists")
	finally:
		db.close()
		
		
db = sq.connect("data/mydb")
db.row_factory = sq.Row
cursor = db.cursor()
cursor.execute(''' SELECT name, email, phone FROM users''')
for row in cursor:
	print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))

db.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
	