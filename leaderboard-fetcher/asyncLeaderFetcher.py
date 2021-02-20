import requests
import signalfx
import json
import time

sfx = signalfx.SignalFx(ingest_endpoint='http://otelcol:9943').ingest('token-at-collector')

def fetchStarShipLeaders():
	

	try:
		r = requests.get("http://leaderboard:6001/leaders/starship")
		leaderboard = json.loads(r.content)
		finalData = []
		for leader in leaderboard:
			leaderScore = {}
			leaderScore["dimensions"] = {}
			leaderScore["dimensions"]["user"]=leader["member"]

			leaderRank = {}
			leaderRank["dimensions"] = {}
			leaderRank["dimensions"]["user"]=leader["member"]

			leaderScore["metric"] = "starship.leaderScore"
			leaderRank["metric"] = "starship.leaderRank"

			leaderScore["value"] = leader["score"]
			leaderRank["value"] = leader["rank"]

			finalData.append(leaderScore)
			finalData.append(leaderRank)

		print('Sending data:',finalData)
		sfx.send(gauges=finalData)

	except:
		print('Ran into problems parsing content')

def asyncLeaderUpdate():
	i = 0
	while i < 2:
		fetchStarShipLeaders()
		time.sleep(10)

asyncLeaderUpdate()


