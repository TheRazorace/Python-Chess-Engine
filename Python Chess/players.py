import random

def random_ai(board):
    
    move = random.choice(list(board.legal_moves))
    return move.uci()


