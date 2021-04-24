import chess


class Board():
    
    def __init__(self):        
        self.board = chess.Board()
        
    def move(self, uci_move):
        return self.board.push_uci(uci_move)
        
    def turn(self, player):
        return "White" if player == chess.WHITE else "Black"
    
    def turn_num(self):
        return len(self.board.move_stack)
    
    def fen(self):
        return self.board.fen()
    
    def legal_moves(self):
        return list(move.uci() for move in self.board.legal_moves)
    
    def legal_fens(self):
        
        current_fen = self.fen()
        fens = []
        moves = self.legal_moves()
        
        for i in range(len(moves)):
            self.move(moves[i])
            next_fen = self.fen()
            fens.append(next_fen)
            self.reset_to_specific(current_fen)
            
        return fens
    
    def reset_to_specific(self, fen):
         self.board = chess.Board(fen)
    
    def reset(self):
        self.__init__()
        
    
    





