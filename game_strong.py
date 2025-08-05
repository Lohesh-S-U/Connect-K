from ConnectState import ConnectState
from mcts import MCTS
from minimax_strong import Minimax_strong

def play():
    k = int(input("Enter k: "))
    print(f"Playing Connect-{k}\n\n")
    state = ConnectState(k)

    algo_choice = input("Choose algorithm to play against (mcts/minimax): ").strip().lower()
    if algo_choice == "mcts":
        ai = MCTS(state)
    elif algo_choice == "minimax":
        depth = int(input("Enter Minimax depth: "))
        ai = Minimax_strong(state, depth)
    else:
        print("Invalid choice. Defaulting to MCTS.")
        ai = MCTS(state)

    while not state.game_over():
        print("Current state:")
        state.print()

        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))

        state.move(user_move)
        ai.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        if algo_choice == "mcts":
            ai.search(8)
            num_rollouts, run_time = ai.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = ai.best_move()
            print("MCTS chose move: ", move)
        elif algo_choice == "minimax":
            move,label = ai.best_move()
            print("Minimax chose move: ", move)
            print("Reason: ", label)

        state.move(move)
        ai.move(move)

        if state.game_over():
            if state.get_outcome() == 2:
                print("Player two won!")
                break
            else:
                print("Draw")
                break

if __name__ == "__main__":
    play()