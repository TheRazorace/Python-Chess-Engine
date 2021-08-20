from board import Board
import numpy as np
from fen_transformation import fen_transform
from move_transformation import move_transform
from tensorflow.keras.models import load_model
import random
import tensorflow as tf

def selfplay(games_simed, model, distributions, selfgames):
    
    sys_random = random.SystemRandom()
    training_set = []
    training_turn_set = []
    training_labels = []
    probability_labels = []
    probability_fens = []
    probability_turns = []
    
    wins = 0
    draws = 0
    losses = 0
    
    
    for match in range(games_simed):
        
        print("Match:", match+1)
        game = Board()
        moves_set = []
        moves = 0
        
        while not game.board.is_game_over(claim_draw = True):
            
            legal_moves = game.legal_moves()
            legal_fens = game.legal_fens()
            prediction_set = []
            turn_set = []
            
            if moves%2 == 0:
                next_turn = -1.0
            else:
                next_turn = 1.0
            
            for i in range(len(legal_fens)):
                fen_table = fen_transform(legal_fens[i])
                prediction_set.append(fen_table)
                turn_set.append(next_turn)
            
            prediction_set = np.asarray(prediction_set)
            turn_set = np.asarray(turn_set)
            #predictions = model.predict([prediction_set,turn_set]).reshape(len(prediction_set))
            predictions = tf.keras.backend.get_value(model([prediction_set, turn_set])).flatten()
            
            if moves%2 == 0:
                best_indices = predictions.argsort()[-(int(len(predictions)/6) + 1):][::-1]
            else:
                best_indices = (-predictions).argsort()[-(int(len(predictions)/6) + 1):][::-1]
                
            weights = distributions[len(best_indices) - 1]
 
            stohastic_choice = sys_random.choices(best_indices, weights=weights)[0]
            
            moves_set.append(prediction_set[stohastic_choice])
            probability_fens.append(fen_transform(game.fen()))
            probability_labels.append(move_transform(legal_moves[stohastic_choice]))
            probability_turns.append(game.turn_int())
            game.move(legal_moves[stohastic_choice])
            moves += 1
            
        result = "draw"
        if game.board.is_checkmate():
            result = not game.board.turn
        
        if result=="draw":
            draws += 1
            
        elif result==False:
            losses += 1
            turn = -1.0
            for i in range(moves):
                training_labels.append(-1.0) 
                training_set.append(moves_set[i])
                training_turn_set.append(turn)
                turn = -1.0*turn
                
        else:
            wins += 1
            turn = -1.0
            for i in range(moves):
                training_labels.append(1.0)
                training_set.append(moves_set[i])
                training_turn_set.append(turn)
                turn = -1.0*turn
                           
                
             
    print("Wins:", wins, "Draws:", draws, "Losses:", losses, "\n")
    
                
    training_set = np.asarray(training_set)
    training_turn_set = np.asarray(training_turn_set)
    training_labels = np.asarray(training_labels)
    probability_labels = np.asarray(probability_labels)
    probability_fens = np.asarray(probability_fens)
    probability_turns = np.asarray(probability_turns)
    new_selfgames = selfgames + losses + wins
    
    # if wins>losses + 2:
    #     training_set = []
    #     training_turn_set = []
    #     training_labels = []
    #     new_selfgames = selfgames
    
    return (training_set, training_turn_set, training_labels, probability_fens,
            probability_turns, probability_labels, new_selfgames)

def create_distributions():
    
    distributions = []
    for length in range(1,50):
        weights = [100]
        prob = 100
        for i in range(1, length):
            prob = prob - int(prob/2.3)
            weights.append(prob)
        distributions.append(weights)
     
    return distributions
        


if __name__ == "__main__":
    
    # game = Board()
    # probability_model = load_model("selftrain_probability_model.h5") 
    # print(probability_model.predict(
    #     [np.asarray([fen_transform(game.fen())]),np.asarray([game.turn_int()])]))
    
    
    distributions = create_distributions()  
    games_simed = 50
    batch_size = 15
    for i in range(40):
        print("\nBatch:", i+1, "\n")
        
        file = open("selfgames3.txt","r+")
        selfgames = int(file.read())
        file.close()
        
        model = load_model("selftrain3_model.h5") 
        probability_model = load_model("selftrain_probability_model.h5") 
        (training_set, training_turn_set, training_labels, probability_fens,
            probability_turns, probability_labels, new_selfgames) = selfplay(games_simed, model,
        distributions, selfgames)
        
        if (len(training_set) > 0):
            model.fit([training_set, training_turn_set], training_labels,
              batch_size=64, epochs=15, verbose=2)
            print("\n")
        probability_model.fit([probability_fens, probability_turns], probability_labels,
              batch_size=164, epochs=15, verbose=2)    
            
        model.save("selftrain3_model.h5")
        probability_model.save("selftrain_probability_model.h5")
        
        file = open("selfgames3.txt","w+")
        file.write(str(new_selfgames))
        file.close()
        


        
    
    
    
