import random
import mcts 
import no_memory_mcts
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

# games_simed = 50
# sims = 500
# turns_simed = 10
# model = models.load_model("selftrain_model")
# mcts = mcts.MCTS(model)
# nm_mcts = no_memory_mcts.NM_MCTS(model)

# memory_wins = 1
# draws = 0
# no_memory_wins = 1
    
# for match in range(2, games_simed):
        
#     print("Match:", match+1)
#     game = Board()
#     moves = 0
    
#     while not game.board.is_game_over(claim_draw = True):
         
#         if moves%2 == 0:
#             player = 1
#             move = mcts.run(player, game, sims, turns_simed)
#         else:
#             player = -1
#             move = nm_mcts.run(player, game, sims, turns_simed)
            
#         game.move(move)
#         moves += 1
        
#     result = "draw"
#     if game.board.is_checkmate():
#         result = not game.board.turn
    
#     if result=="draw":
#         draws += 1
#         print("Draw", draws)
        
#     elif result==False:
#         no_memory_wins += 1
#         print("No-Memory Wins", no_memory_wins)
            
#     else:
#         memory_wins += 1
#         print("Memory Wins", memory_wins)
                       
            
         
# print("Memory Wins:", memory_wins, "Draws:", draws, "No-Memory Wins:", no_memory_wins, "\n")


