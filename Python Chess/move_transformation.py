import tensorflow as tf
from fen_transformation import fen_transform
import numpy as np

squares = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
           'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
           'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
           'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
           'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
           'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
           'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
           'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8']

def move_transform(move):
    
    prob_labels = [0]*128
    start = move[0:2]
    end = move[2:4]
    
    prob_labels[squares.index(start)] = 0.5
    prob_labels[64 + squares.index(end)] = 0.5
    
    return prob_labels

def predict_probability(game, model):
    
    fen_table = fen_transform(game.fen())
    
    prediction_set = []
    prediction_set.append(fen_table)
    prediction_set = np.asarray(prediction_set)
    
    turn_set = []
    turn_set.append(game.turn_int())
    turn_set = np.asarray(turn_set)
    
    probs = tf.keras.backend.get_value(model([prediction_set, turn_set]))[0]
    
    probs_list = []
    for move in game.legal_moves():
        start = move[0:2]
        end = move[2:4]
        probs_list.append(probs[squares.index(start)] + probs[64 + squares.index(end)])
    
    return probs_list


# model = load_model("datatrain_probability_model.h5")
# game = Board()
# predict_probability(game,model)








