import json
import os
import redis

from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient(
    'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ[
        'MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379),
                          db=os.environ.get("REDIS_DB", 0))

games_collection = db.games


@application.route('/')
def index():
    games_collection.delete_many({})
    return render_template('index.html')


@application.route('/game')
def setup():
    games_collection.insert_one({
        "stage": 0,
        "count": 0,
        "guessing": ["", "", "", ""],
        "answer": ["", "", "", ""],
        "hint": ["*", "*", "*", "*"],
        "win": False
    })
    current_game = games_collection.find_one({"win": False})
    return render_template('setup.html', current_game=current_game)


@application.route('/setup', methods=['POST'])
def make_answer():
    current_game = games_collection.find_one({"win": False})
    stage = current_game["stage"]
    answer = current_game["answer"]
    if stage < 4:
        answer[stage] = request.form['answer']
        stage += 1
        games_collection.update({"win": False}, {"$set": {
            "stage": stage,
            "answer": answer
        }})
    return render_template('setup.html', current_game=current_game)


@application.route('/guessing', methods=['GET'])
def get_guessing():
    games_collection.update_one({"win": False}, {"$set": {
        "stage": 0
    }})
    current_game = games_collection.find_one({"win": False})
    return render_template('guessing.html', current_game=current_game)


@application.route('/guessing', methods=['POST'])
def guessing():
    current_game = games_collection.find_one({"win": False})
    stage = current_game["stage"]
    guess = current_game["guessing"]
    hint = current_game["hint"]
    answer = current_game["answer"]
    count = current_game["count"]
    if stage < 4:
        guess[stage] = request.form['guessing']
        count += 1
        if answer[stage] == guess[stage]:
            stage += 1
            hint.pop(0)
            games_collection.update({"win": False}, {"$set": {
                "stage": stage,
                "guessing": guess,
                "hint": hint
            }})
        games_collection.update({"win": False}, {"$set": {
            "count": count
        }})
    if stage == 4:
        games_collection.update({"win": False}, {"$set": {
            "win": True
        }})
    win_data = games_collection.find_one({"win": True})
    return render_template('guessing.html', current_game=current_game, win_data=win_data)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
