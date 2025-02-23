import copy
import random

class CheckersGames:
    def __init__(self):
        self.board = self.init_board()
        self.turn = 'w'

    def init_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        board[row][col] = 'b'
                    elif row > 4:
                        board[row][col] = 'w'
        return board
    
    def getAllMoves(self, player):
        moves = []
        must_capture = False  # prove, if the variable is set
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    continue
                if player == 'w' and piece.lower() == 'w':
                    pieceMoves = self.getPieceMoves(row, col)
                    for move in pieceMoves:
                        if move[2]: 
                            must_capture = True
                    moves.extend(pieceMoves)
                elif player == 'b' and piece.lower() == 'b':
                    pieceMoves = self.getPieceMoves(row, col)
                    for move in pieceMoves:
                        if move[2]: 
                            must_capture = True
                    moves.extend(pieceMoves)
        if must_capture:
            moves = [move for move in moves if move[2]]
        return moves

    
    def getPieceMoves(self, row, col):
        piece = self.board[row][col]
        moves = []
        directions = []
        # normal move: corresponding colour moves forward
        if piece.lower() == 'w':
            directions = [(-1, -1), (-1, 1)]
        if piece.lower() == 'b':
            directions = [(1, -1), (1, 1)]
        # if a "dame" appears, every direction is possible
        if piece.isupper():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            newRow = row + dr
            newCol = col + dc
            # normal push, if the target field is free
            if 0 <= newRow < 8 and 0 <= newCol < 8 and self.board[newRow][newCol] is None:
                moves.append(((row, col), (newRow, newCol), []))
            # punish move, continue one enemy stone
            captureRow = row + 2 * dr
            captureCol = col + 2 * dc
            if 0 <= captureRow < 8 and 0 <= captureCol < 8:
                middlePiece = self.board[newRow][newCol]
                if middlePiece is not None and middlePiece.lower() != piece.lower() and self.board[captureRow][captureCol] is None:
                    moves.append(((row, col), (captureRow, captureCol), [(newRow, newCol)]))
        return moves
    
    def makeMove(self, move):
        (start, end, captured) = move
        sr, sc = start
        er, ec = end
        piece = self.board[sr][sc]
        self.board[sr][sc] = None
        self.board[er][ec] = piece
        for r, c in captured:
            self.board[r][c] = None
        # upgrade to dame by reaching the last row
        if piece == 'w' and er == 0:
            self.board[er][ec] = 'W'
        if piece == 'b' and er == 7:
            self.board[er][ec] = 'B'

    def evaluateBoard(self):
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    continue
                pieceValue = 1 if piece.islower() else 3  # dame is more worthy
                positionValue = 0.1 * (3.5 - abs(3.5 - row))  # bonus for middle part of the board
                if piece.lower() == 'w':
                    score += pieceValue + positionValue
                elif piece.lower() == 'b':
                    score -= pieceValue + positionValue
        return score

    # === Minimax Algorithmus ===
    def minimax(self, depth, maximizingPlayer, alpha, beta):
        if depth == 0:
            return self.evaluateBoard(), None
        
        player = 'w' if maximizingPlayer else 'b'
        moves = self.getAllMoves(player)
        if not moves:
            return self.evaluateBoard(), None
        
        bestMove = None
        if maximizingPlayer:
            maxEval = -float('inf')
            for move in moves:
                newGame = copy.deepcopy(self)
                newGame.makeMove(move)
                eval, _ = newGame.minimax(depth-1, False, alpha, beta)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval, bestMove
        else:
            minEval = float('inf')
            for move in moves:
                newGame = copy.deepcopy(self)
                newGame.makeMove(move)
                eval, _ = newGame.minimax(depth-1, True, alpha, beta)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval, bestMove
    
    # === Monte Carlo Tree Search (MCTS) ===
    def monteCarloTreeSearch(self, simulations):
        possibleMoves = self.getAllMoves('b')
        if not possibleMoves:
            return None

        moveScores = {(start, end, tuple(captured)): 0 for (start, end, captured) in possibleMoves}

        for (start, end, captured) in possibleMoves:
            for _ in range(simulations):
                newGame = copy.deepcopy(self)
                newGame.makeMove((start, end, captured))
                result = newGame.simulateRandomGame()
                moveScores[(start, end, tuple(captured))] += result
    
        bestMove = max(moveScores, key=moveScores.get)
        return [bestMove[0], bestMove[1], list(bestMove[2])]
    
    def simulateRandomGame(self):
        while True:
            moves = self.getAllMoves('w' if self.turn == 'b' else 'b')
            if not moves:
                return 1 if self.turn == 'b' else -1
            randomMove = random.choice(moves)
            self.makeMove(list(randomMove))