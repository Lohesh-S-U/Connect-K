import math
import time
from copy import deepcopy
from ConnectState import ConnectState
from meta import GameMeta

class Minimax_strong:
    def __init__(self, state, depth):
        self.root_state = deepcopy(state)
        self.depth = depth
        self.k = state.k 
        self.dp = {}

    def get_better_moves(self, state):
        legal_moves = state.get_legal_moves()
        scored_moves = []

        for move in legal_moves:
            new_state = deepcopy(state)
            new_state.move(move)
            score = self.score_position(new_state.get_board(), state.to_play)
            scored_moves.append((move, score))

        scored_moves.sort(key=lambda x: x[1], reverse=True)

        sorted_moves = [move for move, score in scored_moves]

        return sorted_moves
    
    def get_hash(self, board):
        player_one_hash = 0
        player_two_hash = 0

        for i in range(GameMeta.COLS):
            player_one = 0
            player_two = 0
            for j in range(GameMeta.ROWS):
                if board[j][i] == GameMeta.PLAYERS['one']:
                    player_one += 2**j
                elif board[j][i] == GameMeta.PLAYERS['two']:
                    player_two += 2**j
            player_one_hash += player_one * (10**i)
            player_two_hash += player_two * (10**i)
                
        return player_one_hash, player_two_hash

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        # Generate a unique hash for the current board state
        player_one_hash, player_two_hash = self.get_hash(state.get_board())
        state_hash = (player_one_hash, player_two_hash, depth, maximizing_player)

        # Check if the result is already in the DP cache
        if state_hash in self.dp:
            return self.dp[state_hash]

        if depth == 0 or state.game_over():
            if state.game_over():
                outcome = state.get_outcome()
                if outcome == state.to_play:
                    return math.inf if maximizing_player else -math.inf
                elif outcome is not None:
                    return -math.inf if maximizing_player else math.inf
            return self.score_position(state.get_board(), state.to_play)

        better_moves = self.get_better_moves(state)
        if maximizing_player:
            max_eval = -math.inf
            for move in better_moves:
                new_state = deepcopy(state)
                new_state.move(move)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.dp[state_hash] = max_eval  # Store the result in the DP cache
            return max_eval
        else:
            min_eval = math.inf
            for move in better_moves:
                new_state = deepcopy(state)
                new_state.move(move)
                eval = self.minimax(new_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.dp[state_hash] = min_eval  # Store the result in the DP cache
            return min_eval

    def best_move(self):
        start_time = time.time()  # Start timing
        legal_moves = self.root_state.get_legal_moves()
        best_score = -math.inf
        best_move = None
        for move in legal_moves:
            new_state = deepcopy(self.root_state)
            new_state.move(move)
            score = self.minimax(new_state, self.depth - 1, -math.inf, math.inf, False)
            if score > best_score:
                best_score = score
                best_move = move
        ori_score, ori_center_score, ori_def_score = self.score_position_helper(self.root_state.get_board(), GameMeta.PLAYERS['two'])
        new_state = deepcopy(self.root_state)
        
        print(new_state.height)
        print(best_move)
        new_state.move(best_move)
        print(new_state.height)

        score, center_score, def_score = self.score_position_helper(new_state.get_board(), GameMeta.PLAYERS['two'])
        score_diff = score - ori_score
        center_score_diff = center_score - ori_center_score
        def_score_diff = def_score - ori_def_score
        print("Score diff: ", score_diff, " Center Score diff:", center_score_diff, " Def Score diff:", def_score_diff, "\n")
        label = "No reason"
        if score_diff >= def_score_diff and score_diff >= center_score_diff:
            label = "Offensive move"
        elif center_score_diff >= score_diff and center_score_diff >= def_score_diff:
            label = "Center move"
        else:
            label = "Defensive move"
        end_time = time.time()  # End timing
        time_taken = end_time - start_time
        print(f"Time Taken: {time_taken:.4f} seconds")  
        return best_move, label

    def move(self, move):
        self.root_state.move(move)

    def score_position(self, board, piece):
        score, center_score, def_score = self.score_position_helper(board, piece)
        return score + center_score - def_score

    def score_position_helper(self, board, piece):
        score = 0
        def_score = 0
        opp_piece = GameMeta.PLAYERS['one'] if piece == GameMeta.PLAYERS['two'] else GameMeta.PLAYERS['two']

        # Score center column
        center_col = GameMeta.COLS // 2
        center_array = [int(row[center_col]) for row in board]
        center_count = center_array.count(piece)
        center_score = center_count * (10 ** (self.k-3))

        # Score Horizontal
        for r in range(GameMeta.ROWS):
            row_array = [int(i) for i in board[r]]
            for c in range(GameMeta.COLS - self.k + 1):
                window = row_array[c:c + self.k]
                score += self.evaluate_window(window, piece)[0]
                def_score += self.evaluate_window(window, piece)[1]

        # Score Vertical
        for c in range(GameMeta.COLS):
            col_array = [int(board[r][c]) for r in range(GameMeta.ROWS)]
            for r in range(GameMeta.ROWS - self.k + 1):
                window = col_array[r:r + self.k]
                score += self.evaluate_window(window, piece)[0]
                def_score += self.evaluate_window(window, piece)[1]

        # Score positive sloped diagonal
        for r in range(GameMeta.ROWS - self.k + 1):
            for c in range(GameMeta.COLS - self.k + 1):
                window = [board[r + i][c + i] for i in range(self.k)]
                score += self.evaluate_window(window, piece)[0]
                def_score += self.evaluate_window(window, piece)[1]

        # Score negative sloped diagonal
        for r in range(GameMeta.ROWS - self.k + 1):
            for c in range(GameMeta.COLS - self.k + 1):
                window = [board[r + self.k - 1 - i][c + i] for i in range(self.k)]
                score += self.evaluate_window(window, piece)[0]
                def_score += self.evaluate_window(window, piece)[1]

        return score, center_score, def_score

    def evaluate_window(self, window, piece):
        score = 0
        def_score = 0
        opp_piece = GameMeta.PLAYERS['one'] if piece == GameMeta.PLAYERS['two'] else GameMeta.PLAYERS['two']

        for i in range(2, self.k + 1):
            if window.count(piece) == i and window.count(0) == self.k - i:
                score += 10 ** (i - 1)

        if window.count(opp_piece) == self.k-1 and window.count(piece) == 1:
            def_score = 10**(self.k-1)

        return score, def_score