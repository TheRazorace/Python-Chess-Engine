from board import Board
import numpy as np
from fen_transformation import fen_transform
from keras import models
import random

def selfplay(games_simed, model, distributions, selfgames):
    
    sys_random = random.SystemRandom()
    training_set = []
    training_labels = []
    
    wins = 0
    draws = 0
    losses = 0
    
    for match in range(games_simed):
        
        print("Match:", match+1)
        game = Board()
        prediction_set = []
        moves_set = []
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
                
 
            weights = distributions[len(best_indices) - 1]
 
            stohastic_choice = sys_random.choices(best_indices, weights=weights)[0]
            
            moves_set.append(prediction_set[stohastic_choice])
            prediction_set = []
            game.move(legal_moves[stohastic_choice])
            moves += 1
            
        result = "draw"
        if game.board.is_checkmate():
            result = not game.board.turn
        
        if result=="draw":
            draws += 1
            
        elif result==False:
            losses += 1
            for i in range(moves):
                training_labels.append(-1.0) 
                training_set.append(moves_set[i])
                
        else:
            wins += 1
            for i in range(moves):
                training_labels.append(1.0)
                training_set.append(moves_set[i])
                           
                
             
    print("Wins:", wins, "Draws:", draws, "Losses:", losses, "\n")
                
    training_set = np.asarray(training_set)
    training_labels = np.asarray(training_labels)
    new_selfgames = selfgames + losses + wins
    
    return training_set, training_labels, new_selfgames

def create_distributions():
    
    distributions = []
    for length in range(1,30):
        weights = [100]
        prob = 100
        for i in range(1, length):
            prob = prob - int(prob/2.5)
            weights.append(prob)
        distributions.append(weights)
     
    return distributions
        


if __name__ == "__main__":
    
    distributions = create_distributions()    
    games_simed = 100
    for i in range(100):
        print("\nBatch:", i+1, "\n")
        
        file = open("selfgames.txt","r+")
        selfgames = int(file.read())
        file.close()
        
        model = models.load_model("selftrain_model") 
        training_set, training_labels, new_selfgames = selfplay(games_simed, model,
        distributions, selfgames)
        
        if (len(training_set) > 0):
            model.fit(training_set, training_labels,
              batch_size=5, epochs=10, verbose=2)
            
        model.save("selftrain_model")
        
        file = open("selfgames.txt","w+")
        file.write(str(new_selfgames))
        file.close()

        
    
    
    
