class AlphaBeta():
    def __init__(self, symbol):
        self.symbol = symbol
        self.max_depth = 0
        self.minimax_calls = 0
        

    def getMove(self, board, prevMove):
        if self.symbol == "X":
            maximizing_player = 1
        else:
            maximizing_player = 0
        alpha = -float('inf')
        beta = float('inf')
        limit = 45
        depth = 0
        return self.alphaBeta(board, alpha, beta, maximizing_player, prevMove, depth, limit)[1]

    def h(self, board):
        board = board.getBoard()
        count_self, count_oppo = 0, 0
        for r in range(0, 3):
            for c in range(0, 3):
                small = board[r][c]
                curState = small.getState()
                if curState[0] == "W":
                    if curState[1] == self.symbol:
                        count_self += 1
                    else:
                        count_oppo += 1
        return count_self - count_oppo

   
    def alphaBeta(self, board, alpha, beta, maximizing_player, prevMove, depth, limit):
        self.minimax_calls += 1
        if depth > self.max_depth:
            self.max_depth = depth
        if depth > limit: 
            return (self.h(board), [-1,-1])

        # Check if the game is over
        curState = board.getState()
        if curState[0] == 'W':
            if curState[1] == 'X':
                # X wins, so return a high score
                return (1.0, prevMove)
            elif curState[1] == 'O':
                return (-1.0, prevMove)
        elif curState[0] == 'D':
            return (0.0, prevMove)

        if maximizing_player == 1:
            # Maximize the score for X
            best_score = -float('inf')
            best_move = None
            nextMoves, nextSymbol = board.getValidMoves(prevMove)
            for move in nextMoves:
                # Make the move
                new_board = board 
                new_board.playMove(move, nextSymbol)
                # Recursively search for the best score with the other player
                (score, nmove) = self.alphaBeta(new_board, alpha, beta, 0, move, depth, limit)
                # Update the best score if necessary
                if score > best_score:
                    best_score = max(best_score, score)
                    best_move = move
                # Update the alpha value
                alpha = max(alpha, best_score)
                # Check for alpha-beta pruning
                if beta <= alpha:
                    break
            # Return the best score
            return (best_score, best_move)
        else:
            # Minimize the score for O
            best_score = float('inf')
            best_move = None
            nextMoves, nextSymbol = board.getValidMoves(prevMove)
            for move in nextMoves:
                # Make the move
                new_board = board
                new_board.playMove(move, nextSymbol)
                # Recursively search for the best score with the other player
                (score, nmove) = self.alphaBeta(new_board, alpha, beta, 1, move, depth, limit)
                # Update the best score if necessary
                if score < best_score:
                    best_score = min(best_score, score)
                    best_move = move
                # Update the beta value
                beta = min(beta, best_score)
                # Check for alpha-beta pruning
                if beta <= alpha:
                    break
            # Return the best score
            return (best_score, best_move)