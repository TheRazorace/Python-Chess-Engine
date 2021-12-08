from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import players   
from board import Board
import time

app = Flask(__name__)
app.secret_key = "prlce_secret_key"

# mcts1 = None
# mcts2 = None
# session["mode"]= None
# session["opponent_model"]= None
# session["selfplay_model1"]= None
# session["selfplay_model2"]= None
# session["time_limit1"]= 5
# session["time_limit2"]= 5
# session["turns_simed"]= 10
player_move = "None"
game = Board()
# color = None
# opp_color = None

def run_app():     
    app.run(debug = True)


@app.route('/', methods = ["POST", "GET"])
def index():
    #global mode, color, opp_color, opponent_model, selfplay_model1, selfplay_model2
    session["reset"] = False
    
    # game = Board()
    # with open('data.pkl', 'wb') as output:
    #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
    session["time_limit1"]= 10
    session["time_limit2"]= 10

    if request.method == "POST":
        session["mode"] = request.form["mode"]
        session["color"] = request.form["color"]
        
        session["opponent_model"] = request.form["opp_model"]
        session["selfplay_model1"] = request.form["sp_model1"]
        session["selfplay_model2"] = request.form["sp_model2"]
        
        if session["color"] == "White":
            session["opp_color"] = "Black"
        else:
            session["opp_color"] = "White"
        
        return redirect(url_for(session["mode"]))
    else:    
        return render_template('index.html')
    

@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."

@app.route('/selfplay')
def selfplay():
    #global session["mcts1"], selfplay_model1, session["mcts2"], selfplay_model2
    # global mcts1, mcts2
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
    
    # mcts1 = players.initialize_mcts(session["selfplay_model1"])
    # mcts2 = players.initialize_mcts(session["selfplay_model2"])
    game.reset() 
    # players.initialize_engine1(session["selfplay_model1"])
    # players.initialize_engine2(session["selfplay_model2"])
    
    # with open('data.pkl', 'wb') as output:
    #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
    time.sleep(5)
           
    return render_template('selfplay.html',
                starting_fen = game.board.fen(),
                model1 = session["selfplay_model1"],
                model2 = session["selfplay_model2"])

@app.route('/versusplay')
def versusplay():
    #global session["mcts1"], color, opponent_model
    # global mcts1
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
    # mcts1 = players.initialize_mcts(session["opponent_model"])
    game.reset()  
    #players.initialize_engine1(session["opponent_model"])
    # with open('data.pkl', 'wb') as output:
    #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
    time.sleep(5)
         
    return render_template('versusplay.html',
        starting_fen = game.board.fen(),
        first_moves = list(move.uci() for move in game.board.legal_moves),
        player_color = session["color"].lower(),
        opponent = session["opponent_model"])


@app.route('/selfmove', methods=['GET', 'POST'])
def selfmove():
    #global session["mcts1"], time_limit1, session["mcts2"], time_limit2, turns_simed
    #global mcts1, mcts2
    
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
        
    while not game.board.is_game_over(claim_draw = True):
        turn = game.turn_str(game.board.turn)
        if turn == "White":
            #uci = players.engine_move(game, mcts1, session["time_limit1"], session["turns_simed"]) 
            uci = players.engine_move(game, session["time_limit1"],  session["selfplay_model1"]) 
        else:
            #uci = players.engine_move(game, mcts2, session["time_limit2"], session["turns_simed"]) 
            uci = players.engine_move(game, session["time_limit2"], session["selfplay_model2"]) 
            
        game.move(uci)
        # with open('data.pkl', 'wb') as output:
        #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)

        # GET request
        if request.method == 'GET':
            message = {'move':uci, 'player': turn,
                       'fen':game.board.fen(), 'isgameover':game.board.is_game_over()}
            return jsonify(message)          
            
    result, msg = check_result()
    if request.method == 'GET':
        message = {'result': result, 'msg': msg}
        return jsonify(message)
    
    game.reset()
    return

@app.route('/get_player_move', methods=['GET', 'POST'])
def get_player_move():
    #global player_move, color, opp_color
    global player_move
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
    #while game.turn_str(game.board.turn) == session["opp_color"]:
        #pass
    while player_move=="None":
        continue
    game.move(player_move)
    isgameover = game.board.is_game_over()
    
    # with open('data.pkl', 'wb') as output:
    #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
            
    # GET player's move
    if request.method == 'GET':
        message = {'move': player_move, 'player': session["color"],
                   'fen':game.board.fen(), 'isgameover': isgameover}
        return jsonify(message)  
             
    return

@app.route('/get_engine_move', methods=['GET', 'POST'])
def get_engine_move():
    #global session["mcts1"], time_limit1, turns_simed, color, opp_color
    #global mcts1
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
    #while game.turn_str(game.board.turn) == session["color"]:
        #pass
    isgameover = game.board.is_game_over()
    if not isgameover:
        #engine_move = players.engine_move(game, mcts1, session["time_limit1"], session["turns_simed"]) 
        engine_move = players.engine_move(game, session["time_limit1"], session["opponent_model"]) 
        game.move(engine_move)
        
        # with open('data.pkl', 'wb') as output:
        #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
        next_moves = list(move.uci() for move in game.board.legal_moves)
        
        # GET engine's move
        if request.method == 'GET':
            message = {'move':engine_move, 'player': session["opp_color"],
                   'fen':game.board.fen(), 'isgameover': isgameover,
                   'legal_moves': next_moves}
            return jsonify(message) 
    
    return

@app.route('/get_result', methods=['GET', 'POST'])
def get_result():
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
        
    isgameover = game.board.is_game_over()
    if isgameover:
        result, msg = check_result()
        if request.method == 'GET':
            message = {'result': result, 'msg': msg}
            return jsonify(message)
        
    return

    
@app.route('/reset', methods=['GET','POST'])
def reset():
    #global opponent_model, session["mcts1"], selfplay_model1, session["mcts2"], selfplay_model2, mode
    #global mcts1, mcts2
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
        
    if request.method == "POST":
        
        # if session["mode"] == "versusplay":
        #     #mcts1 = players.initialize_mcts(session["opponent_model"])
        #     players.initialize_engine1(session["opponent_model"])
        
        # else:
        #     # mcts1 = players.initialize_mcts(session["selfplay_model1"])
        #     # mcts2 = players.initialize_mcts(session["selfplay_model2"])
        #     players.initialize_engine1(session["selfplay_model1"])
        #     players.initialize_engine2(session["selfplay_model2"])
        # time.sleep(3)

        req = request.get_json()
        if req.get("reset") == "true":
            game.reset()
            time.sleep(5)
            # with open('data.pkl', 'wb') as output:
            #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
        return req.get("reset"), 200

    
    
@app.route('/post_move', methods=['GET','POST'])
def post_move():
    global player_move
    
    if request.method == "POST":
        req = request.get_json()
        player_move = req.get("move")
        return player_move, 200

    
def check_result():
    
    # with open('data.pkl', 'rb') as input:
    #     game = pickle.load(input)
        
    result = "draw"
    if game.board.is_checkmate():
        msg = "Checkmate: " + game.turn_str(not game.board.turn) + " wins!"
        result = not game.board.turn
    elif game.board.is_stalemate():
        msg = "Draw: Stalemate"
    elif game.board.is_fivefold_repetition():
        msg = "Draw: 5-fold repetition"
    elif game.board.is_insufficient_material():
        msg = "Draw: Insufficient material"
    elif game.board.can_claim_draw():
        msg = "Draw: Claim"
        
    return result, msg
    
        

if __name__ == "__main__":
    # with open('data.pkl', 'wb') as output:
    #     game = Board()
    #     pickle.dump(game, output, pickle.HIGHEST_PROTOCOL)
    run_app()
    

