from board import Board
import numpy as np
from keras import models

game = Board()

pieces = ['k', 'q', 'r', 'b', 'n', 'p', 'P', 'N', 'B', 'R', 'Q', 'K']
pawn_values = [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
knight_values = [0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
bishop_values = [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
rook_values = [0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
queen_values = [0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
king_values = [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
empty_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def fen_transform(fen):
    
    position_list = []
    row_list = []
    chessboard_list = []

    fen = fen.split(" ")[0]
    fen = fen.split("/")
    for row in fen:
        for char in row:
            if char.isalpha():
                position_list.append(pawn_values[pieces.index(char)])
                position_list.append(knight_values[pieces.index(char)])
                position_list.append(bishop_values[pieces.index(char)])
                position_list.append(rook_values[pieces.index(char)])
                position_list.append(queen_values[pieces.index(char)])
                position_list.append(king_values[pieces.index(char)])
                row_list.append(position_list)

            else:
                position_list = empty_position
                for i in range (int(char)):
                    row_list.append(position_list)
            position_list = []
                    
        chessboard_list.append(row_list)   
        row_list = []         
                    
    fen_table = np.asarray(chessboard_list)

    return fen_table

# =============================================================================
# fen_table = fen_transform(game.fen())
# model = models.load_model("engine_model")
# test_set = np.array([fen_table])
# prediction = model.predict(test_set)
# print(prediction)
# =============================================================================







