from board import Board
import numpy as np
from fen_transformation import fen_transform
from keras import models
import random
from tempfile import TemporaryFile

def selfplay(games_simed):
    
    model = models.load_model("engine_model")
    sys_random = random.SystemRandom()
    
    training_set = []
    training_labels = []
    
    for match in range(games_simed):
    
        game = Board()
        prediction_set = []
        moves = 0
        while not game.board.is_game_over(claim_draw = True):
            
            legal_moves = game.legal_moves()
            legal_fens = game.legal_fens()
            
            for i in range(len(legal_fens)):
                fen_table = fen_transform(legal_fens[i])
                prediction_set.append(fen_table)
            
            prediction_set = np.asarray(prediction_set)
            predictions = model.predict(prediction_set).reshape(len(prediction_set))
            
            if moves%2 == 0:
                best_indices = predictions.argsort()[-(int(len(predictions)/4) + 1):][::-1]
            else:
                best_indices = (-predictions).argsort()[-(int(len(predictions)/4) + 1):][::-1]
                
            weights = [100]
            len_best = len(best_indices)
            prob = 100
            for i in range(1, len_best):
                prob = prob - int(prob/2.5)
                weights.append(prob)
                
            stohastic_choice = sys_random.choices(best_indices, weights=weights)[0]
            
            training_set.append(prediction_set[stohastic_choice])
            prediction_set = []
            game.move(legal_moves[stohastic_choice])
            moves += 1
            
        result = "draw"
        if game.board.is_checkmate():
            result = not game.board.turn
        
        print(match)
        
        if result=="draw":
            for i in range(moves):
                training_labels.append(0.0)
        
        elif result==False:
            for i in range(moves):
                training_labels.append(-1.0)
                
        else:
            for i in range(moves):
                training_labels.append(1.0)
        
    
    training_set = np.asarray(training_set)
    training_labels = np.asarray(training_labels)
    
    with open('training_set.npy', 'wb') as f:
        np.save(f, training_set)
        
    with open('training_labels.npy', 'wb') as f:
        np.save(f, training_labels)
    
    return



if __name__ == "__main__":
    #games_simed = 100
    #selfplay(games_simed)
    
    model = models.load_model("engine_model")
    
    with open('training_set.npy', 'rb') as f:
        training_set = np.load(f)
        
    np.load('training_labels.npy', allow_pickle=True)
        
    model.fit(training_set, training_labels, validation_split=0.1,
          batch_size=40, epochs=100, verbose=2)
    
