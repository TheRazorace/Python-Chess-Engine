import math
import numpy as np
from board import Board

def ucb_score(parent, child):
    
    node_score = child.value()
    prior_score = 1.4 * math.sqrt(
                  math.log(parent.visit_count)/child.visit_count)
    
    return node_score + prior_score

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
    
    def value(self):
        
        if self.visit_count == 0:
            return 0
        
        return self.value_sum/ self.visit_count
    
    
    def select_action(self, temperature):
        
        visit_counts = np.array([child.visit_count for child in self.clidren.values()])
        actions = [action for action in self.children.keys()]
        
        if temperature == 0:
            action = actions[np.argmax(visit_counts)]
        else:
            visit_count_distribution = visit_counts ** (1 / temperature)
            visit_count_distribution = visit_count_distribution / sum(visit_count_distribution)
            action = np.random.choice(actions, p=visit_count_distribution)

        return action
    
    def select_child(self):
        
        best_score = -1000
        
        index = 0
        for child in self.children:
            score = ucb_score(self, child)
            if score > best_score:
                best_score = score
                best_action = self.moves[index]
                best_child = child
            index += 1 
                
        return best_action, best_child
    
    def expand(self, game, player):
        
        self.player = player
        self.state = game.fen()
        
        legal_fens = game.legal_fens()
        for i in range(len(legal_fens)):
            self.children[i] = Node(player = self.player*-1)
            
        return
    
    
class MCTS:
    
    def _init_(self, game, model, games_simed):
        self.game = game
        self.model = model
        self.games_simed = games_simed
        
    def run(self, model, game, player, turns_simed):
        
        root = Node(player)
        game.reset()
        root.expand(game, player)
        
        for i in range(self.sims):
            node = root
            path = [node]
            
            #Select
            while node.expanded():
                action, node = node.select_child()
                game.move(action)
                path.append(node)
            
            parent = path[-2]
            reward = game.state_reward()
            #If game has not ended: Expand
            if reward is None:
                node.expand(game, parent.player * -1)
                fen_table = fen_transform(game.fen())
                prediction_set.append(fen_table)
                prediction_set = np.asarray(prediction_set)
                reward = model.predict(prediction_set).reshape(len(prediction_set))
                
            #Backpropagate
            self.backpropagate(path, reward, parent.player * -1)
                
    return root

    def backpropagate(self, path, reward, player):
        
        for node in reversed(path):
            node.value_sum += reward
            node.visit_count += 1
                
            
                
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


