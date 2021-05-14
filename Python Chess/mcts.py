import numpy as np
from board import Board
from fen_transformation import fen_transform
from keras import models
import random

def ucb_score(parent, child, player):
    
    score = child.value(parent, player)
    
    #print(score)
    return score

class Node:
    
    def __init__(self, player):
        self.visit_count = 0
        self.player = player
        self.value_sum = 0
        self.children = []
        self.moves = []
        self.state = None
        
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
                score = ucb_score(self, child, self.player)
    
                if score > best_score:
                    best_score = score
                    best_action = index
                    best_child = child
                index += 1 
                
        elif self.player==-1:
            for child in self.children:
                score = ucb_score(self, child, self.player)
    
                if score < best_score:
                    best_score = score
                    best_action = index
                    best_child = child
                index += 1
            
                
        return best_action, best_child
    
    def expand(self, game, player):
        
        self.player = player
        self.state = game.fen()
        
        legal_fens = game.legal_fens()
        for i in range(len(legal_fens)):
            self.children.append(Node(player = self.player*-1))
                               
            
        return
    
    
class MCTS:
    
    def __init__(self, game, model, games_simed):
        self.game = game
        self.model = model
        self.sims = games_simed
        
    def run(self, game, model, player, turns_simed):
        
        root = Node(player)
        root.expand(game, player)
        fen = game.fen()
        game.reset_to_specific(fen)
        
        for i in range(self.sims):
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
                node.expand(game, parent.player * -1)
                
                #Simulation
                reward = self.simulate(game, turns_simed)
                 
                if reward is None:
                    fen_table = fen_transform(game.fen())
                    prediction_set.append(fen_table)
                    prediction_set = np.asarray(prediction_set)
                    reward = model.predict(prediction_set).reshape(len(prediction_set))
                    #print()
                    #print(reward)
                
                
            #Backpropagate
            self.backpropagate(path, reward)
            game.reset_to_specific(fen)
         
        
        best_move = self.get_best_move(root, player)
                        
        return best_move

    def backpropagate(self, path, reward):
        
        for node in reversed(path):
            node.value_sum += 5*reward 
            node.visit_count += 1
            
        return

    
    def simulate(self, game, turns_simed):
        
        for i in range(turns_simed):
            reward = game.state_reward()
            if reward is None:
                legal_moves = game.legal_moves()
                game.move(legal_moves[random.randint(0, len(legal_moves)-1)])
            else:
                break
        
        return reward
    
    def get_best_move(self, root, player):
        
        best_avg_value = -np.inf*player
        best_node = 0
        index = 0
        
        if player==1:
            for node in root.children:
                avg_value = node.visit_count
                if avg_value>best_avg_value:
                    best_avg_value = avg_value
                    best_node = index
                index += 1
                
        else:
            for node in root.children:
                avg_value = node.visit_count
                if avg_value>best_avg_value:
                    avg_value = best_avg_value
                    best_node = index
                index += 1
            
            
        return game.legal_moves()[best_node]
        
        
        
             
                
game = Board()
model = models.load_model("selftrain_model")
player = -1 
sims = 1000
turns_simed = 5      
for i in range(3):
    mcts = MCTS(game, model, sims)
    move = mcts.run(game, model, player, turns_simed)
    print(move)
                    
                

                
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


