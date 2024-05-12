import tkinter as tk
from functools import partial
from math import inf
import sys

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.user_score = 0
        self.ai_score = 0

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player
            self.check_winner()

            if not self.winner:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.winner = self.board[i][0]
                return ((i, 0), (i, 1), (i, 2))
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.winner = self.board[0][i]
                return ((0, i), (1, i), (2, i))
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            return ((0, 0), (1, 1), (2, 2))
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][2]
            return ((0, 2), (1, 1), (2, 0))
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            self.winner = 'Tie'

    def restart(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None

# GUI for Tic-Tac-Toe
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)  # Make window non-resizable
        self.game = TicTacToe()

        self.user_color = 'dodgerblue'
        self.ai_color = 'tomato'

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, font=('Helvetica', 24), width=5, height=2, command=partial(self.on_button_click, i, j), disabledforeground="white")
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)
        self.original_color = self.buttons[0][0].cget("background")
        self.update_buttons()
            
        self.restart_button = tk.Button(root, text="Restart", font=('Helvetica', 12), command=self.restart)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky='nsew', pady=5, padx=2)

        self.user_score_label = tk.Label(root, text=f"User: {self.game.user_score}", font=('Helvetica', 12, 'bold'), foreground=self.user_color)
        self.user_score_label.grid(row=4, column=0, padx=10)

        self.ai_score_label = tk.Label(root, text=f"AI: {self.game.ai_score}", font=('Helvetica', 12, 'bold'), foreground=self.ai_color)
        self.ai_score_label.grid(row=4, column=2, padx=10)

        self.winner_label = tk.Label(root, text="", font=('Helvetica', 16, 'bold'))
        self.winner_label.grid(row=5, columnspan=3, pady=10)

        root.protocol("WM_DELETE_WINDOW", self.close_window)

    def on_button_click(self, row, col):
        if not self.game.winner and self.buttons[row][col]['text'] == ' ':
            self.game.make_move(row, col)
            self.update_buttons()

            if not self.game.winner:
                self.ai_make_move()
                self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] != ' ':
                    self.buttons[i][j].configure(state='disabled')
                if self.game.board[i][j] == 'X':
                    self.buttons[i][j].configure(text='X', background=self.user_color)
                elif self.game.board[i][j] == 'O':
                    self.buttons[i][j].configure(text='O', background=self.ai_color)
                else:
                    self.buttons[i][j].configure(text=' ', background=self.original_color)

        winner_line = self.game.check_winner()
        if winner_line:
            for i, j in winner_line:
                self.buttons[i][j].configure(disabledforeground='lightgreen')

            if self.game.winner == 'Tie':
                self.winner_label.configure(text="It's a Tie!", foreground='black')
            else:
                winner = "User" if self.game.winner == 'X' else "AI"
                color = self.user_color if self.game.winner == 'X' else self.ai_color
                self.winner_label.configure(text=f"{self.game.winner} wins ({winner})", foreground=color)

                if self.game.winner == 'X':
                    self.game.user_score += 1
                else:
                    self.game.ai_score += 1

                self.user_score_label.configure(text=f"User: {self.game.user_score}", foreground=self.user_color)
                self.ai_score_label.configure(text=f"AI: {self.game.ai_score}", foreground=self.ai_color)
        else:
            # Check for tie
            if all(self.game.board[i][j] != ' ' for i in range(3) for j in range(3)):
                self.winner_label.configure(text="It's a Tie!", foreground='black')

    def ai_make_move(self):
        best_score = -inf
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.game.board[i][j] == ' ':
                    self.game.board[i][j] = 'O'
                    score = self.minimax(self.game.board, 0, False, -inf, inf)
                    self.game.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.game.make_move(*best_move)

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        game = TicTacToe()
        game.board = board
        game.check_winner()

        if game.winner == 'O':
            return 1
        elif game.winner == 'X':
            return -1
        elif game.winner == 'Tie':
            return 0

        if is_maximizing:
            best_score = -inf
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = 'O'
                        score = self.minimax(game.board, depth + 1, False, alpha, beta)
                        game.board[i][j] = ' '
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = inf
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = 'X'
                        score = self.minimax(game.board, depth + 1, True, alpha, beta)
                        game.board[i][j] = ' '
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def restart(self):
        self.game.restart()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=' ', state='normal', background=self.original_color, disabledforeground='white')
        self.winner_label.configure(text='')

    def close_window(self):
        self.root.destroy()
        sys.exit()

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    TicTacToeGUI(root)
    root.mainloop()
