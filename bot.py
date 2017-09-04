from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import authenticate
import time
import requests
import json
import db

minFollowers = 1500
databaseName = "twitterData.db"
conn = db.connectdb()
initialTime = time.time()

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

class StdOutListener(StreamListener):
	def on_data(self, data):
		dataJson = json.loads(data)
		user = dataJson["user"]
		followers, username, userID = user["followers_count"], user["screen_name"], user["id_str"]
		if followers >= minFollowers:
			print(username + " | " + str(followers))
			if db.db(conn, "check", userID, username, followers):
				action = "update"
			else:
				action = "add"
			db.db(conn, action, userID, username, followers)

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
