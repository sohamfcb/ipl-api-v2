from flask import Flask,jsonify,request
import ipl
import jugaad

app=Flask(__name__)

@app.route('/')
def home():
    return 'Hello'

@app.route('/api/teams')
def teams():
    teams=ipl.teamsAPI()
    return jsonify(teams)

@app.route('/api/teamvteam')
def teamvteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    response=ipl.teamVteamAPI(team1, team2)
    return jsonify(response)

@app.route('/api/team-record')
def team_record():
    team_name=request.args.get('team')
    response=jugaad.teamAPI(team_name)
    return response

@app.route('/api/batsman-record')
def batsman_record():
    batsman_name=request.args.get('batsman')
    response=jugaad.batsmanAPI(batsman_name)
    return response

@app.route('/api/bowler-record')
def bowler_record():
    bowler_name=request.args.get('bowler')
    response=jugaad.bowlerAPI(bowler_name)
    return response

app.run(debug=True)