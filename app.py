from flask import Flask, render_template, jsonify, request
from game import TicTacToe

app = Flask(__name__)
game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data.get('position')

    # Player move
    if not game.make_move(position, 'X'):
        return jsonify({'error': 'Invalid move'}), 400

    # Check if player won
    if game.check_winner():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'winner': 'Player',
            'winning_line': game.get_winning_line()
        })

    # Check for tie
    if game.is_board_full():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'winner': 'Tie'
        })

    # Computer move
    computer_pos = game.computer_move()

    # Check if computer won
    if game.check_winner():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'winner': 'Computer',
            'winning_line': game.get_winning_line(),
            'computer_move': computer_pos
        })

    # Check for tie after computer move
    if game.is_board_full():
        return jsonify({
            'board': game.board,
            'game_over': True,
            'winner': 'Tie',
            'computer_move': computer_pos
        })

    return jsonify({
        'board': game.board,
        'game_over': False,
        'computer_move': computer_pos
    })

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({'board': game.board})

if __name__ == '__main__':
    app.run(debug=True)
