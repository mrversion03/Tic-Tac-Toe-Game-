import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x700")
        self.current_player = 'X'
        self.board = [None] * 9
        self.scores = {'X': 0, 'O': 0, 'draws': 0}
        self.history = []
        self.game_mode = None  # 'pvp' or 'pvb'

        self.create_ui()

    def create_ui(self):
        # Mode selection
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=20)
        tk.Label(self.mode_frame, text="Choose Game Mode", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.mode_frame, text="Player vs Player", width=20, command=lambda: self.start_game('pvp')).pack(pady=5)
        tk.Button(self.mode_frame, text="Player vs Bot", width=20, command=lambda: self.start_game('pvb')).pack(pady=5)

        # Game Frame
        self.game_frame = tk.Frame(self.root)
        self.cells = [tk.Button(self.game_frame, text="", font=("Arial", 24), width=5, height=2,
                                command=lambda i=i: self.click_cell(i)) for i in range(9)]
        for i, btn in enumerate(self.cells):
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)

        # Controls
        self.control_frame = tk.Frame(self.root)
        self.new_game_btn = tk.Button(self.control_frame, text="New Game", command=self.reset_board)
        self.reset_score_btn = tk.Button(self.control_frame, text="Reset Scores", command=self.reset_scores)
        self.back_btn = tk.Button(self.control_frame, text="Change Mode", command=self.back_to_mode)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.score_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.history_label = tk.Label(self.root, text="", font=("Arial", 10), justify="left")

    def start_game(self, mode):
        self.game_mode = mode
        self.mode_frame.pack_forget()
        self.game_frame.pack(pady=20)
        self.control_frame.pack(pady=10)
        self.new_game_btn.pack(side="left", padx=5)
        self.reset_score_btn.pack(side="left", padx=5)
        self.back_btn.pack(side="left", padx=5)
        self.status_label.pack()
        self.score_label.pack()
        self.history_label.pack(pady=10)
        self.reset_board()

    def click_cell(self, index):
        if self.board[index] or self.current_player == 'O' and self.game_mode=='pvb':
            return

        self.board[index] = self.current_player
        self.cells[index].config(text=self.current_player)
        winner = self.check_winner()

        if winner:
            self.end_game(winner)
        elif all(self.board):
            self.end_game('draw')
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.update_status()
            if self.game_mode=='pvb' and self.current_player=='O':
                self.root.after(300, self.bot_move)

    def bot_move(self):
        # Simple AI: win/block or random
        move = self.find_best_move('O') or self.find_best_move('X') or self.random_move()
        if move is not None:
            self.click_cell(move)

    def random_move(self):
        available = [i for i, c in enumerate(self.board) if c is None]
        return random.choice(available) if available else None

    def find_best_move(self, player):
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = player
                if self.check_winner() == player:
                    self.board[i] = None
                    return i
                self.board[i] = None
        return None

    def check_winner(self):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for line in wins:
            a,b,c = line
            if self.board[a] and self.board[a]==self.board[b]==self.board[c]:
                return self.board[a]
        return None

    def end_game(self, winner):
        if winner == 'draw':
            messagebox.showinfo("Draw", "It's a draw!")
            self.scores['draws'] +=1
            self.history.append("Draw")
        else:
            msg = f"{'You' if self.game_mode=='pvb' and winner=='X' else 'Bot' if self.game_mode=='pvb' else 'Player '+winner} Wins!"
            messagebox.showinfo("Winner", msg)
            self.scores[winner] += 1
            self.history.append(msg)
        self.update_status()
        self.update_score()

    def reset_board(self):
        self.board = [None]*9
        for btn in self.cells:
            btn.config(text="")
        self.current_player = 'X'
        self.update_status()

    def reset_scores(self):
        self.scores = {'X':0,'O':0,'draws':0}
        self.history.clear()
        self.update_score()
        self.update_status()

    def back_to_mode(self):
        self.game_frame.pack_forget()
        self.control_frame.pack_forget()
        self.status_label.pack_forget()
        self.score_label.pack_forget()
        self.history_label.pack_forget()
        self.mode_frame.pack(pady=20)
        self.reset_scores()

    def update_status(self):
        self.status_label.config(text=f"Current Turn: {self.current_player}")

    def update_score(self):
        score_text = f"X: {self.scores['X']}   O: {self.scores['O']}   Draws: {self.scores['draws']}\nRecent: {self.history[-5:]}"
        self.score_label.config(text=score_text)
        self.history_label.config(text="\n".join(self.history[-5:]))

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
