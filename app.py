from flask import Flask, jsonify
from pymongo import MongoClient
from models.at_bat.at_bat import AtBat
from models.game.game import Game
from models.player.batter import Batter
from models.player.pitcher import Pitcher
from models.team.team import Team
from models.field.field import Field

from flask import request

# def create_app():
app = Flask(__name__)
client = MongoClient("localhost", 27017)
app.db = client.bbtn

home_team_lineup = Team(
    "Cardinals", [Batter("Patrick", 13, "SS", 4, 3)], Pitcher("Tom", 11, "P", 3, 5)
)
away_team_lineup = Team(
    "Dodgers", [Batter("Mason", 5, "SS", 4, 3)], Pitcher("John", 10, "P", 3, 5)
)
game = None


@app.route("/games", methods=["POST"])
def create_games():
    home_team: Team = home_team_lineup
    away_team: Team = away_team_lineup
    game = Game(home_team, away_team, Field())
    game.save_to_mongo()
    return jsonify(game.json())


@app.route("/games", methods=["GET"])
def get_games():
    return jsonify([game.json() for game in Game.get_games()])


@app.route("/at-bat", methods=["POST"])
def at_bat():
    at_bat = AtBat(
        game, game.home_team.pitcher, game.away_team.lineup[game.away_team.at_bat]
    )
    result = at_bat.pitch(request.form["pitcher_guess"], request.form["batter_guess"])
    at_bat.update_game(game, result)
    return game.__str__()
