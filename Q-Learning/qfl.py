import datetime
from collections import defaultdict
import random

# Takes the allowed CPU time in seconds and
# Returns a function that takes a position and returns the move suggested 
def q_learn(model, cpu_time):
    q_learning = Q_Learning(model)
    begin = datetime.datetime.utcnow()
    while (datetime.datetime.utcnow() - begin) < datetime.timedelta(seconds=cpu_time):
        q_learning.explore()
    def returned_function(pos):
        return q_learning.choose(pos)
    return returned_function

class Q_Learning:
    # initialize 
    def __init__(self, model):
        self.learning_rate = defaultdict(defaultdict)
        self.y = 0.99
        self.q = defaultdict(defaultdict)
        self.x_axis = [2, 6, float('inf')] #1 6/ 2 8[2, 3, float('inf')] .  [1.1, 2.1, 2.6, float('inf')] 
        self.y_axis = [2, 5, float('inf')] # 1 4 
        self.model = model

        # initialize self.q and self.learning_rate
        keys = list(range(0, model.offensive_playbook_size()))
        for x in range(len(self.x_axis)):
            for y in range(len(self.y_axis)):
                self.q[(x,y)] = dict.fromkeys(keys, 0)
                self.learning_rate[(x,y)] = dict.fromkeys(keys, 0.22)

    def get_super_state(self, position):
        yards_to_score, downs_left, distance, ticks = position
        x_val = distance / downs_left
        y_val = yards_to_score / ticks

        x_idx = next(i for i, val in enumerate(self.x_axis) if val >= x_val)
        y_idx = next(i for i, val in enumerate(self.y_axis) if val >= y_val)
        #x_idx = list(filter(lambda i: self.x_axis[i] >= x_val, range(len(self.x_axis))))[0]
        #y_idx = list(filter(lambda i: self.y_axis[i] >= y_val, range(len(self.y_axis))))[0]
        return (x_idx, y_idx)

    def explore(self):
        position = self.model.initial_position()
        while not self.model.game_over(position):
            curr_super_state = self.get_super_state(position)

            # get next move
            random_num = random.random() #
            if random_num <= 0.2:
                action = random.randint(0, self.model.offensive_playbook_size() - 1)
            else: 
                temp = self.q[curr_super_state]
                action = max(temp, key = temp.get)
            next_pos = self.model.result(position, action)[0]
            
            # update q value & learning rate
            learning_rate = self.learning_rate[curr_super_state][action]
            if self.model.game_over(next_pos):
                reward = 1 if self.model.win(next_pos) else -1
                self.q[curr_super_state][action] += learning_rate * (reward - self.q[curr_super_state][action])
            else:
                next_super_state = self.get_super_state(next_pos)
                max_q = max(self.q[next_super_state].values())
                self.q[curr_super_state][action] += learning_rate * (self.y * max_q - self.q[curr_super_state][action])

            self.learning_rate[curr_super_state][action] *= 0.9985
            position = next_pos

    def choose(self, position):
        curr_super_state = self.get_super_state(position)
        temp = self.q[curr_super_state]
        action = max(temp, key = temp.get)
        
        if temp[action] == 0:# check if there are multiple 0
            # e.g. {0: 0.0, 1: 0, 2: 0}
            idx = [key for key in temp if temp[key]==0]
            action = random.randrange(len(idx))
        return action
   