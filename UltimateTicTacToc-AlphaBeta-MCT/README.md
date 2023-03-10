# Ultimate tic-tac-toe - Game Final Project

### Description 

- Team members: Wangyue Zhao, Xinru Li
- The code is about implementing Ultimate tic-tac-toe by using MonteCarloTreeSearch and AlphaBeta algorithms.

### Rule of ultimate tic-tac-toe
- The game is played on a 3x3 grid of smaller tic tac toe boards.
- Players take turns placing their symbol (either an "X" or an "O") on an empty space on one of the small tic tac toe boards.
- The small tic tac toe board that a player must place their symbol on is determined by the location of the opponent's previous move.
-  The game is won by the first player to get three in a row on any of the small tic tac toe boards, or by getting three in a row on the larger tic tac toe board made up of the small boards.
- If all of the spaces on the board are filled and no player has won, the game ends in a draw.

### To Run

```bash
$ make
$ ./TestUltimateTicTacToe number_of_game_to_run
```
The default number of number_of_game_to_run is 100.
Then, continue choosing the agent for each player, between "MCTS", "AlphaBeta", "Random".

### Result
- We first used MCTS with compile time=0.01 second to play Ultimate tic-tac-toe. The  winning percentage over 100 when playing with a random player is average 0.52 (MCTS win rounds / total rounds). 
- We then used Alpha Beta with a simple heuristic searching to depth 45 to play Ultimate tic-tac-toe. The winning percentage over 100 when playing with a random player is average 0.59 (Alpha Beta win rounds / total rounds)
- We finally used  Alpha Beta player to play with MCTS player. The winning percentage over 100 when playing with a random player is 1.00 (Alpha Beta win rounds / total rounds). 


### Author

* Wangyue Zhao
* Xinru Li

### Reference
Game board & RandomBot reference from: 
    - Author:@vaibhav.garg (year). 
    - Date: 4th Aug'20
    - Retrieved from: https://github.com/VAIBHAV-2303/MonteCarloTreeSearch 
