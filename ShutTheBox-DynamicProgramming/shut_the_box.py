import collections
import argparse
import itertools
from re import S
import sys

TWO_DICE_ROLL_PROBABILITY = {1:0, 2:1/36, 3:2/36, 4:3/36, 5:4/36, 6:5/36, 7:6/36, 8:5/36, 9:4/36, 10:3/36, 11:2/36, 12:1/36}
TILES_SUBSET_INDEX = {}
# ALL_TILES_SUBSETS = []

class ShutTheBox(object):
    def __init__(self):
        """
        self.player = player 1 ("--one") or player 2 ("--two")
        self.action = "--expect" or "--move"
        self.tiles_str = tiles in string (123456789)
        self.tiles = tiles in int list ([1,2,3,4,5,6,7,8,9])
        self.p1_score = player 1 score in int
        self.p1_score_index = a dictionary for all possible player 1 scores and its corresponding index in dp table
        self.roll = sum of dice roll

        self.dp1([s][r])= a 2 dimension dp table for player 1
        - s(game state) = 0 ~ number of possible combination of self.tiles
        - r(roll) = 0 ~ 12
        self.dp2([t][s][r]) = a 3 dimensiondp table for player 2
        - t(p1 score) = 0 ~ number of all possible player 1 scores
        - s(game state) = 0 ~ 510 (all possbile combination for tile [1,2,3,4,5,6,7,8,9])
        - r(roll) = 0 ~ 12
        """
        
        if "py" in sys.argv[0]:
            sys.argv.pop(0)

        self.player = sys.argv[0]
        self.action = sys.argv[1]
        self.tiles_str = sys.argv[2]
        self.p1_score = None
        self.roll = None
        if self.player == "--one" and self.action == "--move":
            # e.g. ./ShutTheBox --one --move 146789 9
            self.roll = int(sys.argv[3])
        if self.player == "--two" and self.action == "--move":
            # e.g. ./ShutTheBox --two --move 13456789 17 12
            self.p1_score = int(sys.argv[3])
            self.roll = int(sys.argv[4])
        if self.player == "--two" and self.action == "--expect":
            # e.g. ./ShutTheBox --two --expect 123456789 8
            self.p1_score = int(sys.argv[3])
        
        # Based on tiles ("12345") create a tile list ([1,2,3,4,5])
        self.tiles = []
        for c in self.tiles_str:
            self.tiles.append(int(c))
        
        self.p1_score_index = {}
        self.initializeP1ScoreIndex()
        self.initializeTilesSubset()
        
        if self.player == "--two":
            self.dp2 = self.createDp2()
        elif self.player == "--one":
            self.dp2 = self.createDp2()
            self.dp1 = self.createDp1()

        # Call functions based on given arguments in command
        self.play()

    
    # All possible t (player1's score) based on either: 
    # (1) if player1, all tiles in player1's hand
    # (2) if player2, given p1_score
    def initializeP1ScoreIndex(self):
        unique_p1_score = set()
        if self.player == "--two":
            unique_p1_score.add(self.p1_score)
        elif self.player == "--one":
            for tiles_state in self.findTilesSubset(self.tiles):
                unique_p1_score.add(sum(tiles_state))

        # Initialize the global dictionary for all possible p1 score:
        # key = t (possible p1 score)
        # value = index 
        idx = 0
        for score in unique_p1_score:
            self.p1_score_index[score] = idx
            idx += 1

    # Initialize the global dictionary for all possible tiles subsets for deck [1,2,3,4,5,6,7,8,9]:
    # key = tiles subset
    # value = index 
    def initializeTilesSubset(self):
        global ALL_TILES_SUBSETS 
        ALL_TILES_SUBSETS = self.findTilesSubset([1,2,3,4,5,6,7,8,9])
        for idx in range(len(ALL_TILES_SUBSETS)):
            TILES_SUBSET_INDEX[ALL_TILES_SUBSETS[idx]] = idx

    def createDp1(self):
        p1_tiles_subsets = self.findTilesSubset(self.tiles)      
        dp1 = [[0] * 13 for _ in range(len(TILES_SUBSET_INDEX))] # dp1[s][r]

        for tiles_state in p1_tiles_subsets:
            for r in range(1, 13):
                # Calculate Probability
                if sum(tiles_state) <= 6: # One dice
                    prob = 1/6
                    if r > 6:
                        continue
                else: # sum(tiles_state) > 6:
                    prob = TWO_DICE_ROLL_PROBABILITY[r]
                s = TILES_SUBSET_INDEX[tuple(tiles_state)] # s = index for tiles states
                tiles_to_close_subsets = self.combination_sum(tiles_state, r)
                
                # Close all tiles -> game end
                if sum(tiles_state) == r:
                    dp1[s][r] = 1 * prob
                # Cannot close any tiles -> base case
                elif len(tiles_to_close_subsets) == 0:
                    str_idx = TILES_SUBSET_INDEX[tuple([1,2,3,4,5,6,7,8,9])]
                    t = self.p1_score_index[sum(tiles_state)]
                    p2_expect = sum(self.dp2[t][str_idx])
                    dp1[s][r] = (1 - p2_expect) * prob
                else:
                    # Can close some of the tiles in hand ->  find best solution based on previous dp data
                    max_weight = -1
                    for tiles_to_close in tiles_to_close_subsets:
                        remain_tiles = list(set(tiles_state) - set(tiles_to_close))
                        remain_tiles.sort()
                        if len(remain_tiles) == 0:
                            max_weight = 1
                            continue
                        else:
                            remain_tiles_s = TILES_SUBSET_INDEX[tuple(remain_tiles)]
                            max_weight = max(max_weight, sum(dp1[remain_tiles_s]))
                    dp1[s][r] = max_weight * prob
        
        return dp1

    def createDp2(self):
        dp2 = [[[0] * 13 for _ in range(len(ALL_TILES_SUBSETS))] for _ in range(len(self.p1_score_index))] # dp2[t][s][r]

        for p1_score in self.p1_score_index:
            t = self.p1_score_index[p1_score]
            for tiles_state in ALL_TILES_SUBSETS:
                for r in range(1, 13):
                    # Calculate Probability
                    if sum(tiles_state) <= 6: # One dice
                        prob = 1/6
                        if r > 6:
                            continue
                    else: # sum(tiles_state) > 6:
                        prob = TWO_DICE_ROLL_PROBABILITY[r]
                    s = TILES_SUBSET_INDEX[tuple(tiles_state)] #s = index for tile state
                    tiles_to_close_subsets = self.combination_sum(tiles_state, r)
                    # Close all tiles -> game end
                    if sum(tiles_state) == r:
                        dp2[t][s][r] = 1 * prob
                    # Cannot close any tiles -> base case
                    elif len(tiles_to_close_subsets) == 0:
                        if sum(tiles_state) < p1_score:
                            dp2[t][s][r] = 1 * prob
                        elif sum(tiles_state) == p1_score:
                            dp2[t][s][r] = 0.5 * prob
                        else: 
                            dp2[t][s][r] = 0 * prob
                    else:
                        # Can close some of the tiles in hand ->  find best solution based on previous dp data
                        max_weight = -1
                        for tiles_to_close in tiles_to_close_subsets:
                            remain_tiles = list(set(tiles_state) - set(tiles_to_close))
                            remain_tiles.sort()
                            if len(remain_tiles) == 0:
                                max_weight = 1
                                continue
                            else:
                                remain_tiles_s = TILES_SUBSET_INDEX[tuple(remain_tiles)]
                                max_weight = max(max_weight, sum(dp2[t][remain_tiles_s]))
                        dp2[t][s][r] = max_weight * prob

        return dp2
    
    def expect(self):    
        s = TILES_SUBSET_INDEX[tuple(self.tiles)]
        if self.player == "--one":
            expect = sum(self.dp1[s])
        elif self.player == "--two":
            t = self.p1_score_index[self.p1_score]
            expect = sum(self.dp2[t][s])
        return ('%.6f' % expect)
    
    def move(self):
        tiles_to_close_subsets = self.combination_sum(self.tiles, self.roll)
        # Cannot close any card -> Base Case
        if len(tiles_to_close_subsets) == 0:
            return []
        else:
            max_subset = []
            max_weight = -1
            for tiles_to_close in tiles_to_close_subsets:
                remain_tiles = list(set(self.tiles) - set(tiles_to_close))
                remain_tiles.sort()
                if len(remain_tiles) == 0:
                    max_weight = 1
                    max_subset = tiles_to_close
                    continue
                else:
                    remain_tiles_s = TILES_SUBSET_INDEX[tuple(remain_tiles)]
                    if self.player == "--one":
                        if sum(self.dp1[remain_tiles_s]) >= max_weight:
                            max_subset = tiles_to_close
                        max_weight = max(max_weight, sum(self.dp1[remain_tiles_s]))
                    elif self.player == "--two":
                        t = self.p1_score_index[self.p1_score]
                        if sum(self.dp2[t][remain_tiles_s]) >= max_weight:
                            max_subset = tiles_to_close
                        max_weight = max(max_weight, sum(self.dp2[t][remain_tiles_s]))

            return max_subset
    
    def combination_sum(self, candidates, target):
        # https://leetcode.com/problems/combination-sum/
        results = []
        def backtrack(remain, comb, start):
            if remain == 0:
                # make a deep copy of the current combination
                results.append(list(comb))
                return
            elif remain < 0:
                # exceed the scope, stop exploration.
                return

            for i in range(start, len(candidates)):
                # add the number into the combination
                comb.append(candidates[i])
                # give the current number another chance, rather than moving on
                backtrack(remain - candidates[i], comb, i + 1)
                # backtrack, remove the number from the combination
                comb.pop()
        backtrack(target, [], 0)
        return results
    
    def findTilesSubset(self, s):
        # https://stackoverflow.com/questions/43014681/create-a-list-of-all-the-subsets-of-a-given-list-in-python-3-x
        return [tuple(subset) for i in range(1, len(s) + 1) for subset in itertools.combinations(s, i)]

    def play(self):
        if self.action == "--expect":
            print(self.expect())
        elif self.action == "--move":
            print(self.move())

if __name__ == '__main__':
    game = ShutTheBox()
    
