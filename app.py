from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt,create_refresh_token
import ipl
import jugaad
from sqlalchemy.orm import scoped_session
from db_orm import User, SessionLocal
from blueprints.register import register_bp
from werkzeug.security import check_password_hash
from datetime import timedelta

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="visca_el_barca"
app.config["JWT_BLACKLIST_ENABLED"]=True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"]=timedelta(days=1)

app.register_blueprint(register_bp)

jwt=JWTManager(app=app)

blacklist=set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti=jwt_payload["jti"]
    return jti in blacklist

@app.route('/')
def home():
    return 'Hello'

@app.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    # engine, sessionlocal, Base = connect_to_server()
    username=data.get("username")
    password=data.get("password")

    session=scoped_session(SessionLocal)
    user=session.query(User).filter(User.username==username).first()

    if user and check_password_hash(user.password, password):
        access_token=create_access_token(identity=username, additional_claims={"email":user.email})
        refresh_token=create_refresh_token(identity=username)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    
    else:
        return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/api/teams')
@jwt_required()
def get_teams():
    teams=ipl.teamsAPI()
    return jsonify(teams)

@app.route('/api/teamvteam')
@jwt_required()
def get_teamvteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    response=ipl.teamVteamAPI(team1, team2)
    return jsonify(response)

@app.route('/api/team-record')
@jwt_required()
def get_team_record():
    team_name=request.args.get('team')
    response=jugaad.teamAPI(team_name)
    return response

@app.route('/api/batsman-record')
@jwt_required()
def get_batsman_record():
    batsman_name=request.args.get('batsman')
    response=jugaad.batsmanAPI(batsman_name)
    return response

@app.route('/api/bowler-record')
@jwt_required()
def get_bowler_record():
    bowler_name=request.args.get('bowler')
    response=jugaad.bowlerAPI(bowler_name)
    return response


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user=get_jwt_identity()
    new_access_token=create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti=get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg":"successfully logged out"}), 200

if __name__=="__main__":
    app.run(debug=True)