import sqlite3


def updateUser(c, username, userid, followers):
	c.execute("update users set username = ?, followers = ? where id = ?", (username, followers, userid))

def addUser(c, username, userid, followers):
	c.execute("insert into users values (?, ?, ?)", (userid, username, followers))

def isUser(c, username):
	c.execute("select exists(select 1 from users where username = ?)", (username,)).fetchone()[0]

def db(conn, action, username, userid, followers):
	c = conn.cursor()
	status = 0
	if action == "update":
		updateUser(c, username, userid, followers)
	elif action == "add":
		addUser(c, username, userid, followers)
	elif action == "check":
		return isUser(c, username)
	else:
		status = -1
	conn.commit()
	return status
	
def makedb(dbname = "twitterData.db"):
	conn = sqlite3.connect(dbname)
	c = conn.cursor()
	c.execute("create table users(id text primary key, username text, followers text)")
	conn.commit()
	conn.close()

def connectdb(dbname = "twitterData.db"):
	return sqlite3.connect(dbname)

def printdb(conn = None):
	if conn is None:
		print("No connection or database name passed")
		return None
	c = conn.cursor()
	for entry in c.execute("select * from users"):
		print(entry)
	return None

def deletedb(conn):
	c = conn.cursor()
	c.execute("drop table users")
