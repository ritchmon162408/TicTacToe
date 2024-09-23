import math
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Initialize the game board and other variables
board = [' ' for _ in range(9)]
game_history = []  # List to store game history
game_id = 1  # Counter for game ID
start_time = None  # To track the start time of each game

# Helper functions for game logic
def check_winner(player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),
                      (0, 4, 8), (2, 4, 6)]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def is_board_full():
    return ' ' not in board

def make_move(player, position):
    if board[position] == ' ':
        board[position] = player
        return True
    return False

# Function to calculate the elapsed time
def calculate_elapsed_time(start_time):
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    return elapsed_time.total_seconds()

# Function to log game history with the elapsed time (timer)
def log_game(winner):
    global game_id, start_time
    elapsed_time = calculate_elapsed_time(start_time)
    game_history.append({
        'id': game_id,
        'winner': winner,
        'duration': elapsed_time  # Store elapsed time in seconds
    })
    game_id += 1

# Minimax algorithm for AI (O)
def minimax(board, depth, is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    make_move('O', move)

# Route to render the game
@app.route('/')
def index():
    return render_template('index.html')

# API route for making moves
@app.route('/make_move', methods=['POST'])
def handle_move():
    global start_time
    data = request.json
    player_move = data['position']

    # If this is the first move, record the start time
    if start_time is None:
        start_time = datetime.now()

    if make_move('X', player_move):
        if check_winner('X'):
            log_game('Player')  # Log the winner
            return jsonify({'board': board, 'winner': 'X'})

        if is_board_full():
            log_game('Draw')  # Log a draw
            return jsonify({'board': board, 'winner': 'Draw'})

        # AI move (O)
        best_move()

        if check_winner('O'):
            log_game('Computer')  # Log the winner
            return jsonify({'board': board, 'winner': 'O'})

        if is_board_full():
            log_game('Draw')  # Log a draw
            return jsonify({'board': board, 'winner': 'Draw'})

        return jsonify({'board': board, 'winner': None})

    return jsonify({'error': 'Invalid move'}), 400

# API route for resetting the game
@app.route('/reset_game', methods=['POST'])
def reset_game():
    global board, start_time
    board = [' ' for _ in range(9)]  # Reset the board
    start_time = None  # Reset the start time
    return jsonify({'board': board})

# API route to get the game history
@app.route('/game_history', methods=['GET'])
def get_game_history():
    # Convert duration to a readable format (minutes and seconds)
    formatted_history = []
    for game in game_history:
        minutes, seconds = divmod(game['duration'], 60)
        duration = f"{int(minutes)}m {int(seconds)}s"
        formatted_history.append({
            'id': game['id'],
            'winner': game['winner'],
            'duration': duration
        })
    return jsonify(formatted_history)

if __name__ == '__main__':
    app.run(debug=True)

    app = Flask(__name__)



