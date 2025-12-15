import random

class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_winner = None

    def reset(self):
        self.board = ['' for _ in range(9)]
        self.current_winner = None

    def make_move(self, position, player):
        if self.board[position] == '':
            self.board[position] = player
            if self.check_winner():
                self.current_winner = player
            return True
        return False

    def check_winner(self):
        # combinations of winning
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        for combo in winning_combos:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] != ''):
                return True
        return False

    def get_winning_line(self):
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in winning_combos:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] != ''):
                return combo
        return []

    def is_board_full(self):
        return '' not in self.board

    def computer_move(self):
        # Simple AI: Try to win, block player, or random move

        # Try to win
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                if self.check_winner():
                    self.current_winner = 'O'
                    return i
                self.board[i] = ''

        # Try to block player
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'X'
                if self.check_winner():
                    self.board[i] = 'O'
                    return i
                self.board[i] = ''

        # Take center if available
        if self.board[4] == '':
            self.board[4] = 'O'
            return 4

        # Take a corner
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == '']
        if available_corners:
            pos = random.choice(available_corners)
            self.board[pos] = 'O'
            return pos

        # Take any available space
        available = [i for i in range(9) if self.board[i] == '']
        pos = random.choice(available)
        self.board[pos] = 'O'
        return pos
