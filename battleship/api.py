from http import HTTPStatus

from flask import Flask, jsonify
from tabulate import tabulate

app = Flask(__name__)

game_board = []
@app.route('/battleship', methods=['POST'])
def create_battleship_game():
    game_board = create_board(10,10)
    print(tabulate(game_board))
    return jsonify({}), HTTPStatus.NOT_IMPLEMENTED


@app.route('/battleship', methods=['PUT'])
def shot():
    return jsonify({}), HTTPStatus.NOT_IMPLEMENTED


@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    return jsonify({}), HTTPStatus.NOT_IMPLEMENTED

def create_board(width, height):
    buckets = [[0] * width] * height
    return buckets