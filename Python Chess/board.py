import chess
import chess.svg
import random
import time
from IPython.display import display, HTML, clear_output


class Board():
    
    def __init__(self):        
        self.board = chess.Board()
        
    def move(self, uci_move):
        return self.board.push_uci(uci_move)
        
    def turn(self, player):
        return "White" if player == chess.WHITE else "Black"
        
    def display_board(self):
        return self.board._repr_svg_()
    
    def turn_num(self):
        return len(self.board.move_stack)
        
        
def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()

def play(player1, player2, game):
    
    pause=2
    
    while not game.board.is_game_over(claim_draw = True):
        
        color = game.turn(game.board.turn)
        if color == "White":
            uci = player1(game.board)
        else:
            uci = player2(game.board)
            
        game.move(uci)
        board_stop = game.display_board()
        html = "<b>Move %s %s, Play '%s':</b><br/>%s" %(
            game.turn_num(), color, uci, board_stop)
        
        #clear_output(wait=True)
        #display(HTML(html))
        print(game.board)
        print()
        time.sleep(0.1)
    
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
    print(msg)
            
    return (result, msg) 
            
    
        

if __name__ == "__main__":
    game = Board()
    result, msg = play(random_ai, random_ai, game)
    





