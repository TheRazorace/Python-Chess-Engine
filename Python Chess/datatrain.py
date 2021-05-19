import chess.pgn 
from board import Board

def clean_file(filename):
    
    with open(filename, "r") as f:
        lines = f.readlines()
    with open(filename, "w") as f:
        for line in lines:
            if "[" not in line:
                f.write(line)           
    return


pgn = open("ficsgamesdb_2000.pgn")
c = 0
while True:
    game = chess.pgn.read_game(pgn)
    print(game.headers["Result"])
    if game == '':
        break
    c =+ 1
first_game = chess.pgn.read_game(pgn)
game = Board()
board = first_game.board()
for move in first_game.mainline_moves():
    board.push(move)
    #print(board.fen())
print(first_game.headers["Result"])
print(c)
