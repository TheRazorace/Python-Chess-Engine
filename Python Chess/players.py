import random
import mcts 
import mcts2
from board import Board
from tensorflow.keras.models import load_model

def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()

def initialize_mcts(model_name):
    
    model = load_model(model_name)
    mcts_tree = mcts.MCTS(model)
    
    return mcts_tree

def engine_move(game, mcts_tree, sims, turns_simed):
 
    move = mcts_tree.run(game.turn_int(), game, sims, turns_simed)
    
    return move


games_simed = 50
sims = 400
turns_simed = 10
model1 = load_model("selftrain_model")
model2 = load_model("selftrain2_model")

old_model_wins = 0
draws = 1
new_model_wins = 0
    
for match in range(0, games_simed):
        
    print("Match:", match+1)
    game = Board()
    moves = 0
    mcts_1 = mcts.MCTS(model1)
    mcts_2 = mcts2.MCTS(model2)
    
    while not game.board.is_game_over(claim_draw = True):
         
        if moves%2 == 0:
            player = 1
            move = mcts_1.run(player, game, sims, turns_simed)
        else:
            player = -1
            move = mcts_2.run(player, game, sims, turns_simed)
            
        game.move(move)
        moves += 1
        print(moves)
        
    result = "draw"
    if game.board.is_checkmate():
        result = not game.board.turn
    
    if result=="draw":
        draws += 1
        print("Draw", draws)
        
    elif result==False:
        new_model_wins += 1
        print("New Model Wins", new_model_wins)
            
    else:
        old_model_wins += 1
        print("Old Model Wins", old_model_wins)
                       
            
         
print("Old model Wins:", old_model_wins, "Draws:", draws, "New model Wins:", new_model_wins, "\n")


