from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import authenticate
import time
import requests
import json
import sqlite3

minFollowers = 1500
databaseName = "twitterData.db"

def getKeysAndSecrets():
	keyFile = open("keys.json", "r")
	keys = json.loads(keyFile.read())
	keyFile.close()

	return keys["akey"], keys["asecret"], keys["ckey"], keys["csecret"]

def createConnection(fileName):
	try:
		conn = sqlite3.connect(fileName)
		return conn
	except Error as e:
		print(e)

	return None

def updateUser(c, username, userid, followers):
	query = "update users set id = ?, followers = ? where username = ?"
	c.execute(query, (userid, followers, username))
	conn.commit()

def addUser(c, username, userid, followers):
	query = "insert into users values (?, ?, ?)"
	c.execute(query, (username, userid, followers))
	conn.commit()

def isUser(c, username):
	query = "select exists(select 1 from users where username = ?)"
	exists = c.execute(query, (username,)).fetchone()[0]
	return exists

conn = createConnection(databaseName)
c = conn.cursor()
initialTime = time.time()

def createConnection(fileName):
	try:
		conn = sqlite3.connect(fileName)
		return conn
	except Error as e:
		print(e)

	return None

class StdOutListener(StreamListener):
	def on_data(self, data):
		dataJson = json.loads(data)
		user = dataJson["user"]
		followers, username, userID = user["followers_count"], user["screen_name"], user["id_str"]
		print(username)
		if followers >= minFollowers:
			if isUser(c, username):
				updateUser(c, username, userID, followers)
			else:
				addUser(c, username, userID, followers)
		if time.time() - initialTime > 60:
			print("I have been running for 5 minutes, shutting down")
			conn.commit()
			conn.close()
			exit()
		return True
	def on_error(self, data):
		print (status)

if __name__ == "__main__":

	accessKey, accessSecret, consumerKey, consumerSecret = getKeysAndSecrets()

	l = StdOutListener()
	auth = OAuthHandler(consumerKey, consumerSecret)
	auth.set_access_token(accessKey, accessSecret)
	stream = Stream(auth, l)

	stream.filter(track = ["python"])
