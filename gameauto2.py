from ConnectState import ConnectState
from minimax_strong import Minimax_strong
from minimax_medium import Minimax_medium

def play():
    k = int(input("Enter k: "))
    print(f"Playing Connect-{k}\n\n")
    state = ConnectState(k)
    
    depth_strong = int(input("Enter Minimax depth for strong solver: "))
    depth_weak = int(input("Enter Minimax depth for medium solver: "))
    strong_ai = Minimax_strong(state, depth_strong)
    weak_ai = Minimax_medium(state, depth_weak)

    current_player = "strong" 

    while not state.game_over():
        print("Current state:")
        state.print()

        print("Thinking...")

        if current_player == "strong":
            move = strong_ai.best_move()
            print("Strong Minimax chose move: ", move)
            state.move(move)
            weak_ai.move(move)
            current_player = "weak"
        elif current_player == "weak":
            move = weak_ai.best_move()
            print("Medium Minimax chose move: ", move)
            state.move(move)
            strong_ai.move(move)
            current_player = "strong"

        if state.game_over():
            state.print()
            outcome = state.get_outcome()
            if outcome == 1:
                print("Player one (Strong Minimax) won!")
            elif outcome == 2:
                print("Player two (Medium Minimax) won!")
            else:
                print("Draw")
            break

if __name__ == "__main__":
    play()