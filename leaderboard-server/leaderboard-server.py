from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import simplejson as json
from leaderboard.leaderboard import Leaderboard
import uwsgidecorators
import signalfx

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

highscore_lb_starship = Leaderboard('highscores-starship',host='redis-instance')


sfx = signalfx.SignalFx(ingest_endpoint='http://otelcol:9943').ingest('token-at-collector')    
    


def parseData(row):
    metricDump1 = {}
    counterArray = []

    metricDump1["dimensions"] = {}
    metricDump1["dimensions"]["ip"] = row["ip"]  # dimension

    metricDump1["metric"] = "starship.shots"
    metricDump1["value"] = row["shots"]

    counterArray.append(metricDump1)

    print('Sending data:',counterArray)

    sfx.send(counters=counterArray)


@app.route('/health')
def health():
    return '{"status":"OK"}', 200

@app.route('/leaders/<game>')
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def returnLeaders(game):
    if game == "starship":
        return json.dumps(highscore_lb_starship.all_leaders()), 200
    return '{}', 200

@app.route('/submitScores', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','application/json'])
def submitScores():
    content = request.get_json(force=True)
    print('Content:',content)

    if "game" in content:
        if content["game"]=="starship":
            highscore_lb_starship.rank_member(content["aduser"], content["score"])
         
    return '{"status":"OK"}', 200


@app.route("/get_my_ip", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def get_my_ip():
    if 'X-Real-Ip' in request.headers:
        return jsonify({'ip':request.headers['X-Real-Ip']}), 200
    else:
        return jsonify({'ip':'-'}), 200
    #return json.dumps({k:v for k, v in request.headers.items()}), 200

@app.route('/submitShots', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','application/json'])
def submitShots():
    content = request.get_json(force=True)
    print('Content:',content)

    shotSubmission = {}

    totalShots = 0
    if "game" in content:
        if content["game"]=="starship":
            if "shots" in content:
                totalShots = content["shots"]

    shotSubmission["shots"] = totalShots

    if 'X-Real-Ip' in request.headers:
        shotSubmission["ip"] = request.headers['X-Real-Ip']        
    else:
        shotSubmission["ip"] = "-"

    parseData(shotSubmission)    
            
         
    return '{"status":"OK"}', 200 


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)
