import chess.pgn 
import numpy as np
from board import Board
from fen_transformation import fen_transform
from tensorflow.keras.models import load_model
from move_transformation import move_transform


def get_pgn_data(pgn, batch_size, datagames, combined_games, parsed):
    
    training_set = []
    training_turn_set = []
    training_labels = []
    probability_fens = []
    probability_turns = []
    probability_labels = []
    eof = False
    
    for match in range(batch_size):
        print("Game:", match+1)
        game = chess.pgn.read_game(pgn)
        if game == None:
            eof = True
            print("End of file!!!")
            break
        parsed += 1
        
        game_copy = game
        board = game_copy.board()
        turn = 1.0
        for move in game_copy.mainline_moves():
            fen_table = fen_transform(board.fen())
            
            probability_fens.append(fen_table)
            probability_turns.append(turn)
            probability_labels.append(move_transform(str(move)))
            board.push(move)
            turn = -1.0*turn
        
        if(game.headers["Result"] == "1/2-1/2"):
            continue
        elif(game.headers["Result"] == "1-0"):
            result = 1.0
        elif(game.headers["Result"] == "0-1"):
            result = -1.0
        else:
            print("\nNo result reported!")
            eof = True
            break
    
        
        board = game.board()
        turn = -1.0
        for move in game.mainline_moves():
            board.push(move)
            fen_table = fen_transform(board.fen())
            
            training_set.append(fen_table)
            training_labels.append(result)
            training_turn_set.append(turn)
            turn = -1.0*turn
            
            # print(board.fen())
            # print(board.turn_int())
        
        datagames += 1
        combined_games += 1
        # eof = True
        # break
    
    training_set = np.asarray(training_set)
    training_turn_set = np.asarray(training_turn_set)
    training_labels = np.asarray(training_labels)
    probability_labels = np.asarray(probability_labels)
    probability_fens = np.asarray(probability_fens)
    probability_turns = np.asarray(probability_turns)
        
    return (training_set, training_turn_set, training_labels,
            probability_fens, probability_turns, probability_labels,
            datagames, combined_games, parsed, eof) 


if __name__ == "__main__":
    
    pgn = open("ficsgamesdb_2004.pgn")
    eof = False
    batch_size = 50
    batch = 1
    
    file = open("games_parsed.txt","r+")
    parsed = int(file.read())
    file.close()
        
    print("Skipping already analyzed games...")
    for match in range(parsed):
        game = chess.pgn.read_game(pgn)
     
    print("Examining rest of file...\n")
    while eof == False:
        
        print("\nBatch:", batch)
        file = open("datagames.txt","r+")
        datagames = int(file.read())
        file.close()
        
        file = open("combinedgames.txt","r+")
        combined_games = int(file.read())
        file.close()
        
        (training_set, training_turn_set, training_labels,
          probability_fens, probability_turns, probability_labels,
        new_datagames, new_combined_games, new_parsed, eof) = get_pgn_data(
        pgn, batch_size, datagames, combined_games, parsed)
            
        model1 = load_model("datatrain_model.h5") 
        #model2 = load_model("combined_model.h5") 
        
        probability_model1 = load_model("datatrain_probability_model.h5") 
        #probability_model2 = load_model("combined_probability_model.h5") 
        
        if (len(training_set) > 0):
            print("\nModel 1:")
            model1.fit([training_set, training_turn_set], training_labels,
              batch_size=32, epochs=15, verbose=1)
            # print("\nModel 2:")
            # model2.fit([training_set, training_turn_set], training_labels,
            #   batch_size=32, epochs=15, verbose=1)
            print("\nProbability Model 1:")
            probability_model1.fit([probability_fens, probability_turns], probability_labels,
              batch_size=100, epochs=40, verbose=1)
            # print("\nProbability Model 2:")
            # probability_model2.fit([probability_fens, probability_turns], probability_labels,
            #   batch_size=100, epochs=15, verbose=1)
            
        model1.save("datatrain_model.h5")
        #model2.save("combined_model.h5")
        
        probability_model1.save("datatrain_probability_model.h5")
        #probability_model2.save("combined_probability_model.h5")
        
        file = open("datagames.txt","w+")
        file.write(str(new_datagames))
        file.close()
        
        # file = open("combinedgames.txt","w+")
        # file.write(str(new_combined_games))
        # file.close()
        
        file = open("games_parsed.txt","w+")
        file.write(str(new_parsed))
        file.close()
        
        batch += 1
        parsed = new_parsed
        
    pgn.close()
    
    # pgn = open("ficsgamesdb_2001.pgn")
    # game = chess.pgn.read_game(pgn)
    # board = game.board()
    # for move in game.mainline_moves():
    #     print(str(move))
    # #board.push(move)
        
        
    
# c = 0
# while True:
#     game = chess.pgn.read_game(pgn)
#     print(game.headers["Result"])
#     if ((game == '') or (c==10)):
#         break
#     c += 1
# print(c)