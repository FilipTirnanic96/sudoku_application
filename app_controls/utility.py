import re
import string
from typing import List

from PyQt5.QtWidgets import QLineEdit, QMessageBox


def get_cell_color(cell: QLineEdit):
    """Extract the background color from the cell's styleSheet."""
    style = cell.styleSheet()
    match = re.search(r"background-color:\s*([^;]+);", style)
    return match.group(1) if match else "No color found"


def update_cell_color_style(cell: QLineEdit, new_color: string):
    """Update the cell color while removing any previous color setting."""
    # Get the existing stylesheet
    current_style = cell.styleSheet()

    # Remove any existing background-color setting
    new_style = []
    for style in current_style.split(";"):
        if not (("background-color" in style.strip()) or ('' == style.strip())):
            new_style.append(style.strip())

    # Add the new background color
    new_style.append(f"background-color: {new_color};")

    # Apply the updated style
    cell.setStyleSheet("; ".join(new_style))


def update_cell_text_color(cell: QLineEdit, new_color: string):
    """Update the text color of a cell."""
    # Get the existing stylesheet
    current_style = cell.styleSheet()

    # Remove any existing color setting
    new_style = []
    for style in current_style.split(";"):
        if not (("color" in style.strip()) or ('' == style.strip())):
            new_style.append(style.strip())
        if "background-color" in style.strip():
            new_style.append(style.strip())

    # Add the new text color
    new_style.append(f"color: {new_color};")

    # Apply the updated style
    cell.setStyleSheet("; ".join(new_style))


def reset_cell_color_style(board: List[List]):
    """Reset board cell color to white."""
    for row in range(9):
        for col in range(9):
            update_cell_color_style(board[row][col], "white")


def find_cell_position(cell: QLineEdit, board: List[List]) -> (int, int):
    """Finds the row and column of a QLineEdit in QGridLayout."""
    for r in range(9):
        for c in range(9):
            if cell == board[r][c]:
                return r, c
    return None, None  # Not found


def is_in_board(cell: QLineEdit, board: List[List]) -> bool:
    for row in board:
        if cell in row:
            return True
    return False


def show_failure_message():
    """Show a message box when the player loses."""
    msg = QMessageBox()
    msg.setWindowTitle("Game Over")
    msg.setText("You made 3 mistakes and lost this game.")
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()  # Show the message box


def show_sudoku_solved_message(elapsed_time: string):
    """Shows popup message if sudoku if solved"""
    msg = QMessageBox()
    msg.setWindowTitle("Sudoku Solved!")
    msg.setText(f"Congratulations! You've solved the Sudoku in {elapsed_time}.")
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def has_zero(board):
    """Check if there is a zero value in the Sudoku board."""
    for row in board:
        if 0 in row:
            return True  # Found a zero
    return False  # No zeros found


def find_populated_numbers(board):
    """Returns a list of numbers (1-9) that appear exactly 9 times in the board."""
    count = {num: 0 for num in range(1, 10)}  # Initialize count for numbers 1-9

    for row in board:
        for cell in row:
            if cell in count:
                count[cell] += 1  # Count occurrences of each number

    # Find numbers that appear exactly 9 times
    populated_numbers = [num for num, freq in count.items() if freq == 9]
    return populated_numbers
