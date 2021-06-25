import numpy as np
from board import Board
from fen_transformation import fen_transform
from tensorflow.keras.models import load_model
import random
import tensorflow.keras.backend as keras_backend
import pandas as pd
import time
np.seterr(divide = 'ignore') 

class Node:
    
    def __init__(self, player, state):
        self.visit_count = 0
        self.player = player
        self.value_sum = 0
        self.children = []
        self.state = state
        
    def expanded(self):
        return len(self.children) > 0
    
    def value(self, parent, player):
        
        if self.visit_count == 0:
            return player*np.inf            
            
        node_score = self.value_sum/ self.visit_count
        prior_score = 1.4* np.sqrt(
                np.log(parent.visit_count)/self.visit_count)
        return node_score + player*prior_score
    
    
    def select_child(self):
        
        best_score = -self.player*np.inf
        best_action = 0
        best_child = self.children[0]
        
        index = 0
        
        if self.player==1:
            for child in self.children:
                score = child.value(self, 1)
    
                if score > best_score:
                    best_score = score
                    best_action = index
                    best_child = child
                index += 1 
                
        elif self.player==-1:
            for child in self.children:
                score = child.value(self, -1)
    
                if score < best_score:
                    best_score = score
                    best_action = index
                    best_child = child
                index += 1
            
                
        return best_action, best_child
    
    def expand(self, game, player, visited_df):
        
        self.player = player
        
        legal_fens = game.legal_fens()
        for i in range(len(legal_fens)):
            if legal_fens[i] in visited_df['fen'].values:
                self.children.append(visited_df.loc[visited_df['fen'] == legal_fens[i]]['node'].values[0])
            else:    
                self.children.append(Node(self.player*-1, legal_fens[i]))
                               
            
        return 
    
    
class MCTS:
    
    def __init__(self, model):
        self.model = model
        self.visited_df = pd.DataFrame(columns = ['node', 'fen'])
        
    def run(self, player, game, time_limit, turns_simed):
        
        fen = game.fen()
        time_start = time.time() + time_limit
        sims = 0
        
        #visited_df = pd.DataFrame(columns = ['node', 'fen'])
        
        if fen in self.visited_df['fen'].values:
            root = self.visited_df.loc[self.visited_df['fen'] == fen]['node'].values[0]
        
        else:
            root = Node(player, fen)
            self.visited_df.loc[len(self.visited_df.index)] = (root, fen)
            root.expand(game, player, self.visited_df)
        
        while(time.time() < time_start):
            #print("sim", i+1)
            prediction_set = []
            node = root
            path = [node]
            
            #Select
            while node.expanded():
                #print()
                #print("row:", row)
                action, node = node.select_child()
                game.move(game.legal_moves()[action])
                #print(action)
                path.append(node)
            
            parent = path[-2]
            reward = game.state_reward()
            #If game has not ended: Expand
            if reward is None:
                
                if node.state not in self.visited_df['fen'].values:
                    node.expand(game, parent.player * -1, self.visited_df)
                    self.visited_df.loc[len(self.visited_df.index)] = (node, game.fen())
                
                #Simulation
                reward = self.simulate(game, turns_simed)
                 
                if reward is None:
                    fen_table = fen_transform(game.fen())
                    prediction_set.append(fen_table)
                    prediction_set = np.asarray(prediction_set)
                    reward = keras_backend.get_value(self.model(prediction_set))[0][0]
                    #print()
                    #print(reward)
                
                
            #Backpropagate
            self.backpropagate(path, reward)
            game.reset_to_specific(fen)
            sims += 1
         
        best_move = self.get_best_move(root, game)
                        
        return best_move

    def backpropagate(self, path, reward):
        
        for node in reversed(path):
            node.value_sum += 20*reward 
            node.visit_count += 1
            
        return

    
    def simulate(self, game, turns_simed):
        
        for i in range(turns_simed):
            reward = game.state_reward()
            if reward is None:
                legal_moves = game.legal_moves()
                if len(legal_moves) > 0:
                    game.move(legal_moves[random.randint(0, len(legal_moves)-1)])
                else:
                    reward = 0
                    return reward
            else:
                return reward
        
        return reward
    
    def get_best_move(self, root, game):
        
        best_avg_value = -np.inf
        best_node = 0
        index = 0
        
        for node in root.children:
            avg_value = node.visit_count
            if avg_value>best_avg_value:
                best_avg_value = avg_value
                best_node = index
            index += 1       
            
        return game.legal_moves()[best_node]
        
        
        
             
                
# game = Board()
# model = load_model("selftrain_model")
# #model2 = load_model("selftrain2_model")
# player = 1 
# time_limit = 5
# turns_simed = 10 
# mcts = MCTS(model)
# # for i in range(3):
# move, num = mcts.run(player, game, time_limit, turns_simed)
# print(num)


# legal_moves = game.legal_moves()
# legal_fens = game.legal_fens()
# prediction_set = []
# turn_set = []
# for i in range(len(legal_fens)):
#     fen_table = fen_transform(legal_fens[i])
#     prediction_set.append(fen_table)
#     turn_set.append(0)
    
# prediction_set = np.asarray(prediction_set)
# turn_set = np.asarray(turn_set)
# predictions = model.predict(prediction_set).reshape(len(prediction_set))
# predictions2 = model2.predict([prediction_set, turn_set]).reshape(len(prediction_set))
# print(legal_moves)
# print(predictions)

# best_indices = predictions.argsort()[-(int(len(predictions)/4) + 1):][::-1]
# best_indices2 = predictions2.argsort()[-(int(len(predictions)/4) + 1):][::-1]
# for i in best_indices:
#     print(legal_moves[i])
    
# print()
# for i in best_indices2:
#     print(legal_moves[i])