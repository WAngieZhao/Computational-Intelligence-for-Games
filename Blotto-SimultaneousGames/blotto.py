import scipy.optimize
import sys
import itertools
import random

class Solution(object):
    """
    self.mode = "--find" or "--verify"
    self.tolerance = set to 10^(-6) by default
    self.objective = "--win", "--socre", "--lottery"
    self.military_units = number of military units available in int
    self.battlefields = battlefiled score in int list
    self.matrix = payoff matrix for player 1
    self.play = all possible distribution based on given number of military_units and number of battlefields
    self.input = input list for --verify command, generated from the output of --find command
    """
    def __init__(self):
        try:
            argv_lst = sys.argv
            if "py" in argv_lst[0]:
                argv_lst.pop(0)
            self.mode = argv_lst.pop(0) # find / verify

            # Set tolerance to default or match the arguments
            self.tolerance = 10 ** (-6)
            if "tolerance" in argv_lst[0]:
                argv_lst.pop(0)
                self.tolerance = float(argv_lst.pop(0))
            self.objective = argv_lst.pop(0)   # win / score / lottery

            if self.mode == "--find":
                argv_lst.pop(0)  # "--units"
                self.military_units = int(argv_lst.pop(0))

            self.battlefields = [eval(i) for i in argv_lst]
            self.matrix = None
            self.play = None
        except:
            raise Exception("Make Sure to do valid input")

        self.run()
               
    def run(self):
        if self.mode == "--find":
            self.set_play()
            self.calculate_matrix()
            x_result = self.linear_programming()

            # Format output
            for i in range(len(self.play)):
                if x_result[i] != 0:
                    argv_lst = list(self.play[i]) + [x_result[i]]
                    argv_lst = [str(x) for x in argv_lst]
                    print(','.join(argv_lst))

        elif self.mode == "--verify":
            # Read the output from --find as the input
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            self.input = []
            for line in lines:
                argv_lst = line.split(",")
                argv_lst = [eval(i) for i in argv_lst]
                self.input.append(argv_lst)

            self.military_units = sum(self.input[0][:-1])
            self.set_play()
            print(self.verify())
    
    # Initialize self.play
    # Find all possible distribution based on given number of military_units and number of battlefields
    def set_play(self):
        unit_range = []
        for i in range(0, self.military_units + 1):
            unit_range.append(i)
        self.play = sorted(self.k_sum(unit_range, len(self.battlefields), self.military_units))

    # Setup and calculate matrix
    def calculate_matrix(self):
        self.matrix = [[0]*len(self.play) for _ in range(len(self.play))]
        for p2 in range(len(self.play)):
            for p1 in range(len(self.play)):
                self.matrix[p2][p1] = (-1) * self.calculate_payoff(self.play[p1], self.play[p2]) 

    # Calculate the payoff number in the matrix based on objective
    def calculate_payoff(self, p1_play, p2_play):
        p1_score, p2_score = 0, 0
        if self.objective == "--lottery":
            for i in range(len(p1_play)):
                u1 = p1_play[i]
                u2 = p2_play[i]
                if u1 == 0 and u2 == 0:
                    p1_score += float(self.battlefields[i] / 2)
                else:
                    p1_score += float(u1**2 / (u1**2 + u2**2)) * self.battlefields[i]
            return p1_score
        
        for i in range(len(p1_play)):
            if p1_play[i] > p2_play[i]:
                p1_score += self.battlefields[i]
            elif p1_play[i] == p2_play[i]:
                p1_score += float(self.battlefields[i] / 2)
                p2_score += float(self.battlefields[i] / 2)
            elif p1_play[i] < p2_play[i]:
                p2_score += self.battlefields[i] 
        if self.objective == "--win":
            if p1_score == p2_score:    return 0.5
            elif p1_score > p2_score:    return 1
            elif p1_score < p2_score:    return 0
        else: # "--score"
            return p1_score

    # Use linear programming to calculate the weight of each strategy
    def linear_programming(self):
        a1 = self.matrix
        b_ub = [-1.0] * len(self.play)
        c = [1.0] * len(self.play)
        result = scipy.optimize.linprog(c, a1, b_ub, None, None)
        value = 1.0 / result.fun
        x = [xi * value for xi in result.x]
        # Filter out strategies that are below the tolerance
        for x_i in x:
            if x_i < self.tolerance:
                x_i = 0
        return x
        
    def verify(self):
        target = 0
        if self.objective == "--win":
            target = 0.5 - self.tolerance
        else:
            target = sum(self.battlefields)/2 - self.tolerance

        for p2_play in (self.play):
            p1_sum = 0
            for p1_play in (self.input):
                p1_prob = p1_play[-1]
                p1_score = self.calculate_payoff(p1_play[:-1], p2_play)
                p1_sum += p1_prob * p1_score
            if p1_sum < target:
                return "FAIL"
        return "PASSED"
    
    def k_sum(self, A, k, target):
        # https://www.jiuzhang.com/problem/k-sum-ii/
        def dfs(A, index, k, target, subset, subsets):
            if k == 0 and target == 0:
                subsets.append(list(subset))
                return
            if k == 0 or target <= 0:
                return
            for i in range(index, len(A)):
                subset.append(A[i])
                dfs(A, i, k - 1, target - A[i], subset, subsets)
                subset.pop()

        A = sorted(A)
        subsets = []
        dfs(A, 0, k, target, [], subsets)

        ans = []
        for lst in subsets:
            ans += list(itertools.permutations(lst))
        return list(set(ans))
    

if __name__ == '__main__':
    sol = Solution()