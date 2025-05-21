from flask import Flask, request, jsonify, render_template
import chess
import chess.engine  # optional if using Stockfish or others
import random

app = Flask(__name__)
board = chess.Board()

# class AgentFormData:
#     def __init__(self,agentList, selectedWhiteAgent = None, selectedBlackAgent = None):
#         self.agentList = agentList
#         selectedWhiteAgent = selectedWhiteAgent
#         selectedBlackAgent = selectedBlackAgent


@app.route('/', methods =['GET','POST'])
def index():
    agentList = ['Minimax','MCTS','XGBoost', 'Neural Network']
    selectedWhiteAgent = selectedBlackAgent = None

    if request.method == 'POST':
        selectedWhiteAgent = request.form['whiteAgent']
        selectedBlackAgent = request.form['blackAgent']
        print(selectedBlackAgent,selectedWhiteAgent)
    formData = {
        "agentList"          : agentList,
        "selectedWhiteAgent" : selectedWhiteAgent, 
        "selectedBlackAgent" : selectedBlackAgent
        }

    return render_template('index.html',formData= formData)

@app.route('/move', methods=['POST'])
def player_move():
    data = request.get_json()
    move_uci = data.get('move')

    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)

            # --- Your AI logic goes here ---
            ai_move = get_random_ai_move()
            board.push(ai_move)

            return jsonify({'ai_move': ai_move.uci()})
        else:
            return jsonify({'error': 'Illegal move'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    board.reset()
    return jsonify({'status': 'Board reset'})

def get_random_ai_move():
    return random.choice(list(board.legal_moves))

if __name__ == '__main__':
    app.run(debug=True)
