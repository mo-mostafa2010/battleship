from http import HTTPStatus

from flask import Flask, jsonify, request

from tabulate import tabulate

import numpy as np

app = Flask(__name__)

game_board = []
ships = []


@app.route('/battleship', methods=['POST'])
def create_battleship_game():
    ships = request.json['ships']
    # create the board with 10*10 dimmenssion 
    create_board(10,10)
    # fill the ships array with ships from API
    set_ships(ships)
    #Loop in each ship to check if its ok and draw
    for ship in ships:
        #check if ship is in range of board
        if check_ship_range(ship):
            #check if ship is not overlapped with other
            if check_ship_overlap(ship):
                #draw the ship on board
                draw_ship(ship)
            else:
                #respond with overlaped
                return jsonify({"message": "Overlaped"}), HTTPStatus.BAD_REQUEST
                break
        else:
            #respond with out of range
            return jsonify({"message": "Out of range"}), HTTPStatus.BAD_REQUEST
            break
    print(tabulate(game_board, tablefmt="grid"))
    return jsonify({"message": "OK"}), HTTPStatus.OK


@app.route('/battleship', methods=['PUT'])
def shot():
    x = request.json['x']
    y = request.json['y']
    #check if shot is out of range
    if check_shot_range(request.json):
        #filter all ships and get if the shot hits any of ships from the end
        val = list(filter(lambda d: d['x'] == x and d['y'] == y, ships))
        if len(val):
            #if yes send SINK
            sink_ship(val[0])
            shot = 'SINK'
        else:
            #if NOT check if there is a sinked one or even not or water
            shot = 'WATER' if game_board[y][x] == 0 else 'HIT'
        print(tabulate(game_board, tablefmt="grid"))
        return jsonify({'result': shot}), HTTPStatus.OK
    else:
        return jsonify({"message": "Out of range"}), HTTPStatus.BAD_REQUEST


@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    global game_board
    global ships
    #empty all board and ships array to start a new game
    game_board = []
    ships = []
    #print the game board
    print(tabulate(game_board, tablefmt="grid"))
    return jsonify({"message": "OK"}), HTTPStatus.OK

def create_board(width, height):
    global game_board
    #initializ the board with a numpy array filed with zeros 
    game_board = np.full((width, height), 0, dtype=int)
    return game_board

def set_ships(shipsArray):
    global ships
    #set ship variable
    ships = shipsArray

def draw_ship(ship):
    global game_board
    x = ship['x']
    y = ship['y']
    size = ship['size']
    #draw ship as 1 on the board 
    if ship['direction'] == 'H':
        game_board[y][x: (x+size)] += 1
    if ship['direction'] == 'V':
        game_board[y: (y+size):,x] += 1

def sink_ship(ship):
    global game_board
    global ships
    #remove the ship from ships array 
    ships.remove(ship)
    x = ship['x']
    y = ship['y']
    size = ship['size']
    #sink ship as -1 on the board
    if ship['direction'] == 'H':
        game_board[y][x: (x+size)] = -1
    if ship['direction'] == 'V':
        game_board[y: (y+size):,x] = -1

def check_ship_range(ship):
    global game_board
    x = ship['x']
    y = ship['y']
    size = ship['size']
    #check ship range and make sure it`s on board
    if ship['direction'] == 'H':
        valid = (y < len(game_board) and (x + size) < len(game_board[0]))
    if ship['direction'] == 'V':
        valid = ((y + size) < len(game_board) and x < len(game_board[0]))
    return valid

def check_ship_overlap(ship):
    global game_board
    x = ship['x']
    y = ship['y']
    size = ship['size']
    #make sure that there is no overlapping between ships
    if ship['direction'] == 'H':
        valid = 1 not in game_board[y][x: (x+size)]
    if ship['direction'] == 'V':
        valid = 1 not in game_board[y: (y+size):,x]
    return valid


def check_shot_range(shot):
    global game_board
    x = shot['x']
    y = shot['y']
    #check shot range that its on board
    valid = (y < len(game_board) and x < len(game_board[0]))
    return valid
