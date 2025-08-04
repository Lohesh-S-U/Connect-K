import math
import time
from copy import deepcopy
from ConnectState import ConnectState
from meta import GameMeta

class Minimax_weak:
    def __init__(self, state, depth):
        self.root_state = deepcopy(state)
        self.depth = depth
        self.k = state.k  
    
    def minimax(self,state,depth,maximizingPlayer):
        if depth==0 or state.game_over():
            if state.game_over():
                if state.get_outcome()==GameMeta.PLAYERS['two']:
                    return (None,math.inf)
                elif state.get_outcome()==GameMeta.PLAYERS['one']:
                    return (None,-math.inf)
                else:
                    return (None,0)
            else:
                return (None,self.score_position(state.get_board(),GameMeta.PLAYERS['two']))
        
        if maximizingPlayer:
            value = -math.inf
            column = 0
            for col in state.get_legal_moves():
                new_state = deepcopy(state)
                new_state.move(col)
                new_score = self.minimax(new_state,depth-1,False)[1]
                if(new_score>value):
                    value = new_score
                    column = col
            return column,value
        
        else:
            value = math.inf
            column = 0
            for col in state.get_legal_moves():
                new_state = deepcopy(state)
                new_state.move(col)
                new_score = self.minimax(new_state,depth-1,True)[1]
                if(new_score<value):
                    value = new_score
                    column = col
            return column,value



    def best_move(self):
        start_time = time.time()
        best_move, eval = self.minimax(self.root_state,self.depth,True)
        ori_score, ori_center_score, ori_def_score = self.score_position_helper(self.root_state.get_board(), GameMeta.PLAYERS['two'])
        new_state = deepcopy(self.root_state)
        new_state.move(best_move)
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
        end_time = time.time()  
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