import random
import no_memory_mcts
import prob_mcts
# import mcts
# import numpy as np
# import mcts2
from board import Board
from tensorflow.keras.models import load_model
# from fen_transformation import fen_transform
# import tensorflow.keras.backend as keras_backend

# mcts1 = 1
# mcts2 = 1

def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()

# def initialize_engine1(model_name):
#     global mcts1 
    
#     model = load_model(model_name)
#     mcts1 = mcts.MCTS(model)
    
#     return 

# def initialize_engine2(model_name):
#     global mcts2
    
#     model = load_model(model_name)
#     mcts2 = mcts.MCTS(model)
    
#     return 

# def engine1_move(game, sims, turns_simed, model_name):
#     #global mcts1
    
#     move = mcts1.run(game.turn_int(), game, sims, turns_simed)
    
#     return move

def engine_move(game, time_limit, turns_simed, model_name):
    #global mcts2
    
    model = load_model(model_name)
    mcts_tree = no_memory_mcts.NM_MCTS(model)
    move = mcts_tree.run(game.turn_int(), game, time_limit, turns_simed)
    
    return move

# model = load_model("selftrain2_model.h5")
# moves = 0
# game = Board()

# legal_moves = game.legal_moves()
# legal_fens = game.legal_fens()
# prediction_set = []
# turn_set = []
     
# next_turn = 1.0
      
    
# for i in range(len(legal_fens)):
#     fen_table = fen_transform(legal_fens[i])
#     prediction_set.append(fen_table)
#     turn_set.append(next_turn)

# prediction_set = np.asarray(prediction_set)
# turn_set = np.asarray(turn_set)
# predictions = model.predict([prediction_set,turn_set]).reshape(len(prediction_set))
# #predictions = model([prediction_set,turn_set])

# print(legal_moves)
# print(predictions)

games_simed = 50
time_limit = 8
turns_simed = 10
model1 = load_model("datatrain_model.h5")
model2 = load_model("datatrain_model.h5")
prob_model = load_model("datatrain_probability_model.h5")

old_model_wins = 0
draws = 0
new_model_wins = 0
    
for match in range(0, games_simed):
        
    print("Match:", match+1)
    game = Board()
    moves = 0
    mcts_1 = no_memory_mcts.NM_MCTS(model1)
    mcts_2 = prob_mcts.NM_MCTS(model2, prob_model)
    
    while not game.board.is_game_over(claim_draw = True):
         
        if moves%2 == 0:
            move = mcts_1.run(1, game, time_limit, turns_simed)
        else:
            move = mcts_2.run(-1, game, time_limit, turns_simed)
            
        game.move(move)
        moves += 1
        # prediction_set = [ fen_transform(game.fen())]
        # prediction_set = np.asarray(prediction_set)
        # turn = [game.turn_int()]
        # turn_set = np.asarray(turn)
        # print(moves, float(keras_backend.get_value(model2([prediction_set, turn_set]))[0][0]))
        print(moves)
        
    result = "draw"
    if game.board.is_checkmate():
        result = not game.board.turn
    
    if result=="draw":
        draws += 1
               
    elif result==False:
        new_model_wins += 1 
            
    else:
        old_model_wins += 1
        
    print("\nOld Model Wins", old_model_wins) 
    print("Draw", draws)                   
    print("New Model Wins", new_model_wins, "\n")     
         
print("Old model Wins:", old_model_wins, "Draws:", draws, "New model Wins:", new_model_wins, "\n")





