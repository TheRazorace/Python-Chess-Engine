import random
import mcts 
import no_memory_mcts
from board import Board
from keras import models

def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()

games_simed = 50
sims = 500
turns_simed = 10
model = models.load_model("selftrain_model")
mcts = mcts.MCTS(model)
nm_mcts = no_memory_mcts.NM_MCTS(model)

memory_wins = 0
draws = 0
no_memory_wins = 0
    
for match in range(games_simed):
        
    print("Match:", match+1)
    game = Board()
    moves = 0
    
    while not game.board.is_game_over(claim_draw = True):
         
        if moves%2 == 0:
            player = 1
            move = mcts.run(player, game, sims, turns_simed)
        else:
            player = -1
            move = nm_mcts.run(player, game, sims, turns_simed)
            
        game.move(move)
        moves += 1
        
    result = "draw"
    if game.board.is_checkmate():
        result = not game.board.turn
    
    if result=="draw":
        draws += 1
        print("Draw")
        
    elif result==False:
        no_memory_wins += 1
        print("No-Memory Wins")
            
    else:
        memory_wins += 1
        print("Memory Wins")
                       
            
         
print("Memory Wins:", memory_wins, "Draws:", draws, "No-Memory Wins:", no_memory_wins, "\n")
            
    


