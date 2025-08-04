from ConnectState import ConnectState
from mcts import MCTS
from minimax_strong import Minimax

def play():
    k = int(input("Enter k: "))
    print(f"Playing Connect-{k}\n\n")
    state = ConnectState(k)
    
    depth = int(input("Enter Minimax depth: "))
    mcts_ai = MCTS(state)
    minimax_ai = Minimax(state, depth)

    current_player = "mcts" 

    while not state.game_over():
        print("Current state:")
        state.print()

        print("Thinking...")

        if current_player == "mcts":
            mcts_ai.search(8)
            num_rollouts, run_time = mcts_ai.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = mcts_ai.best_move()
            print("MCTS chose move: ", move)
            state.move(move)
            minimax_ai.move(move)
            current_player = "minimax"
        elif current_player == "minimax":
            move = minimax_ai.best_move()
            print("Minimax chose move: ", move)
            state.move(move)
            mcts_ai.move(move)
            current_player = "mcts"

        if state.game_over():
            state.print()
            outcome = state.get_outcome()
            if outcome == 1:
                print("Player one (MCTS) won!")
            elif outcome == 2:
                print("Player two (Minimax) won!")
            else:
                print("Draw")
            break

if __name__ == "__main__":
    play()