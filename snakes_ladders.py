import tkinter as tk
from tkinter import messagebox
import random

# --- Game Data ---

SNAKES = {
    99: 54,
    70: 55,
    52: 42,
    25: 2
}

LADDERS = {
    6: 25,
    11: 35,
    40: 65,
    60: 85
}

BOARD_SIZE = 10       # 10x10
CELL_SIZE = 60        # pixel size of each cell
MARGIN = 40           # margin around board


class SnakesAndLaddersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")

        self.canvas_width = BOARD_SIZE * CELL_SIZE + 2 * MARGIN
        self.canvas_height = BOARD_SIZE * CELL_SIZE + 2 * MARGIN

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white"
        )
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        # Bottom panel for controls
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.BOTTOM, pady=10)

        self.info_label = tk.Label(
            control_frame, text="Player 1's turn", font=("Arial", 14))
        self.info_label.grid(row=0, column=0, padx=10)

        self.dice_label = tk.Label(
            control_frame, text="Dice: -", font=("Arial", 14))
        self.dice_label.grid(row=0, column=1, padx=10)

        self.roll_button = tk.Button(
            control_frame,
            text="Roll Dice",
            font=("Arial", 14),
            command=self.roll_dice
        )
        self.roll_button.grid(row=0, column=2, padx=10)

        # Player positions
        self.player_positions = [0, 0]  # [player1, player2]
        self.current_player = 0         # 0 -> Player 1, 1 -> Player 2

        # Draw the board and players
        self.draw_board()
        self.create_players()

    # --- Board & Graphics ---

    def draw_board(self):
        # Draw grid and numbers
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = MARGIN + col * CELL_SIZE
                y1 = MARGIN + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                # Alternate background color
                if (row + col) % 2 == 0:
                    fill_color = "#f2f2f2"
                else:
                    fill_color = "#d9d9d9"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=fill_color, outline="black")

                # Calculate board number (1–100)
                board_row_from_bottom = BOARD_SIZE - 1 - row
                number = board_row_from_bottom * BOARD_SIZE + col + 1

                self.canvas.create_text(
                    x1 + 5,
                    y1 + 5,
                    text=str(number),
                    anchor="nw",
                    font=("Arial", 8)
                )

        # Draw ladders (green lines) and snakes (red lines)
        for start, end in LADDERS.items():
            self.draw_line_between_cells(start, end, "green")

        for start, end in SNAKES.items():
            self.draw_line_between_cells(start, end, "red")

    def draw_line_between_cells(self, start, end, color):
        x1, y1 = self.get_cell_center(start)
        x2, y2 = self.get_cell_center(end)
        self.canvas.create_line(x1, y1, x2, y2, width=4,
                                fill=color, arrow=tk.LAST)

    def get_cell_center(self, position):
        """Return (x, y) center of the cell for a given board position 1–100."""
        if position < 1:
            # Off-board (start position)
            return MARGIN - CELL_SIZE // 2, self.canvas_height - MARGIN + CELL_SIZE // 2

        position = min(position, 100)
        pos_index = position - 1
        row_from_bottom = pos_index // BOARD_SIZE
        col = pos_index % BOARD_SIZE

        # convert to canvas coordinates
        row = BOARD_SIZE - 1 - row_from_bottom
        x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
        return x, y

    def create_players(self):
        # Player 1: red, Player 2: blue
        x1, y1 = self.get_cell_center(0)
        x2, y2 = self.get_cell_center(0)

        # Slight offset so they don't overlap completely
        self.player_tokens = [
            self.canvas.create_oval(
                x1 - 10, y1 - 10, x1 + 10, y1 + 10, fill="red"),
            self.canvas.create_oval(
                x2 + 10, y2 - 10, x2 + 30, y2 + 10, fill="blue")
        ]

    def move_player_token(self, player_index):
        position = self.player_positions[player_index]
        x, y = self.get_cell_center(position)

        if player_index == 0:
            # Position token slightly left
            x_offset = -10
        else:
            # Position token slightly right
            x_offset = 10

        self.canvas.coords(
            self.player_tokens[player_index],
            x + x_offset - 10,
            y - 10,
            x + x_offset + 10,
            y + 10
        )

    # --- Game Logic ---

    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {roll}")

        player_num = self.current_player
        current_pos = self.player_positions[player_num]

        # Tentative move
        new_pos = current_pos + roll
        if new_pos > 100:
            # Can't move, need exact roll
            self.info_label.config(
                text=f"Player {player_num + 1} needs exact roll to reach 100!"
            )
            self.switch_turn()
            return

        # Check for snakes and ladders
        if new_pos in LADDERS:
            new_pos = LADDERS[new_pos]
        elif new_pos in SNAKES:
            new_pos = SNAKES[new_pos]

        # Update position
        self.player_positions[player_num] = new_pos
        self.move_player_token(player_num)

        # Check for win
        if new_pos == 100:
            messagebox.showinfo(
                "Game Over", f"Player {player_num + 1} wins! 🎉")
            self.roll_button.config(state=tk.DISABLED)
            self.info_label.config(
                text=f"Player {player_num + 1} is the winner!")
            return

        # Switch turn
        self.switch_turn()

    def switch_turn(self):
        self.current_player = 1 - self.current_player
        self.info_label.config(text=f"Player {self.current_player + 1}'s turn")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakesAndLaddersGame(root)
    root.mainloop()
