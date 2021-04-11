from flask import Flask, render_template, request, jsonify
import chess
import chess.svg
import random

class Board():
    
    def __init__(self):        
        self.board = chess.Board()
        
    def move(self, uci_move):
        return self.board.push_uci(uci_move)
        
    def turn(self, player):
        return "White" if player == chess.WHITE else "Black"
    
    def turn_num(self):
        return len(self.board.move_stack)
    
    def reset(self):
        self.__init__()
        
        
def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()

app = Flask(__name__)
game = Board()   

def run_app():
    app.run(debug = True)
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."

@app.route('/selfplay')
def selfplay():
    game.reset()       
    return render_template('selfplay.html', starting_fen = game.board.fen())

@app.route('/versusplay')
def versusplay():
    game.reset()       
    return render_template('versusplay.html',
           starting_fen = game.board.fen(),
           first_moves = list(move.uci() for move in game.board.legal_moves))


@app.route('/selfmove', methods=['GET', 'POST'])
def selfmove():
    
    while not game.board.is_game_over(claim_draw = True):
        color = game.turn(game.board.turn)
        if color == "White":
            uci = random_ai(game.board)
        else:
            uci = random_ai(game.board) 
            
        game.move(uci)

        # GET request
        if request.method == 'GET':
            message = {'move':uci, 'player': color,
                       'fen':game.board.fen(), 'isgameover':game.board.is_game_over()}
            return jsonify(message)          
            
    result, msg = check_result()
    if request.method == 'GET':
        message = {'result': result, 'msg': msg}
        return jsonify(message)
    
    game.reset()
    return

player_move = None
@app.route('/get_player_move', methods=['GET', 'POST'])
def get_player_move():
    global player_move
    
    while game.turn(game.board.turn) == "Black":
        pass
    game.move(player_move)
    isgameover = game.board.is_game_over()
    
    # GET player's move
    if request.method == 'GET':
        message = {'move':player_move, 'player': "White",
                   'fen':game.board.fen(), 'isgameover': isgameover}
        return jsonify(message)  
             
    return

@app.route('/get_engine_move', methods=['GET', 'POST'])
def get_engine_move():
    
    while game.turn(game.board.turn) == "White":
        pass
    isgameover = game.board.is_game_over()
    if not isgameover:
        engine_move = random_ai(game.board) 
        game.move(engine_move)
        next_moves = list(move.uci() for move in game.board.legal_moves)
        
        # GET engine's move
        if request.method == 'GET':
            message = {'move':engine_move, 'player': "Black",
                   'fen':game.board.fen(), 'isgameover': isgameover,
                   'legal_moves': next_moves}
            return jsonify(message) 
    
    return

@app.route('/get_result', methods=['GET', 'POST'])
def get_result():
    
    isgameover = game.board.is_game_over()
    if isgameover:
        result, msg = check_result()
        if request.method == 'GET':
            message = {'result': result, 'msg': msg}
            return jsonify(message)
        
    return
    
@app.route('/reset', methods=['GET','POST'])
def reset():
    
    if request.method == "POST":

        req = request.get_json()
        if req.get("reset") == "true":
            game.reset()
        return req.get("reset"), 200
    
@app.route('/post_move', methods=['GET','POST'])
def post_move():
    global player_move
    
    if request.method == "POST":
        req = request.get_json()
        player_move = req.get("move")
        return player_move, 200
    
def check_result():
    
    result = "draw"
    if game.board.is_checkmate():
        msg = "checkmate: " + game.turn(not game.board.turn) + " wins!"
        result = not game.board.turn
    elif game.board.is_stalemate():
        msg = "draw: stalemate"
    elif game.board.is_fivefold_repetition():
        msg = "draw: 5-fold repetition"
    elif game.board.is_insufficient_material():
        msg = "draw: insufficient material"
    elif game.board.can_claim_draw():
        msg = "draw: claim"
        
    return result, msg
    
        

if __name__ == "__main__":
    run_app()
    

