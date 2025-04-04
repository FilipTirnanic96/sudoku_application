import re
from typing import List, Tuple

from PyQt5.QtWidgets import QLineEdit, QMessageBox


def get_cell_color(cell: QLineEdit) -> str:
    """
    Extract the background color from the QLineEdit's styleSheet.

    Args:
        cell (QLineEdit): A QLineEdit widget representing a cell in the Sudoku board.

    Returns:
        str: The background color of the cell as a string (e.g., 'red', 'white').
             Returns "No color found" if no background-color is set.
    """
    # Get the cell's current style sheet
    style = cell.styleSheet()

    # Use regex to extract the background color from the style sheet
    match = re.search(r"background-color:\s*([^;]+);", style)
    return match.group(1) if match else "No color found" # Return the background color or a default message


def update_cell_color_style(cell: QLineEdit, new_color: str):
    """
    Update the background color of the cell by removing any previous color setting.

    Args:
        cell (QLineEdit): A QLineEdit widget representing a cell in the Sudoku board.
        new_color (str): The new background color to set for the cell (e.g., 'red', 'blue').
    """
    # Get the existing style sheet of the cell
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


def update_cell_text_color(cell: QLineEdit, new_color: str):
    """
    Update the text color of the cell by removing any previous color setting.

    Args:
        cell (QLineEdit): A QLineEdit widget representing a cell in the Sudoku board.
        new_color (str): The new text color to set for the cell (e.g., 'black', 'red').
    """
    # Get the existing stylesheet
    current_style = cell.styleSheet()

    # Remove any existing color setting
    new_style = []
    for style in current_style.split(";"):
        if not (("color" in style.strip()) or ('' == style.strip())):
            new_style.append(style.strip())
        if "background-color" in style.strip():
            new_style.append(style.strip())  # Keep the background color intact

    # Add the new text color
    new_style.append(f"color: {new_color};")

    # Apply the updated style
    cell.setStyleSheet("; ".join(new_style))


def reset_cell_color_style(board: List[List[QLineEdit]]):
    """
    Reset the background color of all cells in the board to white.

    Args:
        board (List[List[QLineEdit]]): A 2D list representing the Sudoku board, where each element is a QLineEdit cell.
    """
    for row in range(9):
        for col in range(9):
            update_cell_color_style(board[row][col], "white") # Set each cell's background color to white


def find_cell_position(cell: QLineEdit, board: List[List[QLineEdit]]) -> Tuple[int, int]:
    """
    Find the row and column position of a given QLineEdit cell in the Sudoku board.

    Args:
        cell (QLineEdit): The QLineEdit widget whose position is to be found.
        board (List[List[QLineEdit]]): A 2D list representing the Sudoku board, where each element is a QLineEdit cell.

    Returns:
        Tuple[int, int]: The row and column position of the cell in the board (0-indexed).
                         Returns (None, None) if the cell is not found.
    """
    # Iterate through the board to find the matching cell
    for r in range(9):
        for c in range(9):
            if cell == board[r][c]:
                return r, c
    return -1, -1  # Not found


def show_failure_message():
    """
    Display a message box when the player loses the game due to 3 mistakes.

    Returns:
        None: This function only shows a message box and does not return any value.
    """
    msg = QMessageBox()
    msg.setWindowTitle("Game Over")
    msg.setText("You made 3 mistakes and lost this game.")
    msg.setIcon(QMessageBox.Critical)
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()  # Show the message box


def show_sudoku_solved_message(elapsed_time: str):
    """
    Display a message box when the Sudoku puzzle is solved, showing the elapsed time.

    Args:
        elapsed_time (str): The time taken by the player to solve the Sudoku.

    Returns:
        None: This function only shows a message box and does not return any value.
    """
    msg = QMessageBox()
    msg.setWindowTitle("Sudoku Solved!")
    msg.setText(f"Congratulations! You've solved the Sudoku in {elapsed_time}.")
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def has_zero(board: List[List[int]]) -> bool:
    """
    Check if there are any zero values (empty cells) in the Sudoku board.

    Args:
        board (List[List[int]]): A 2D list representing the Sudoku board.

    Returns:
        bool: True if there is at least one zero, otherwise False.
    """
    for row in board:
        if 0 in row:
            return True  # Found a zero
    return False  # No zeros found


def find_populated_numbers(board: List[List[int]]) -> List[int]:
    """
    Returns a list of numbers (1-9) that appear exactly 9 times on the board.

    Args:
        board (List[List[int]]): A 2D list representing the Sudoku board, where each cell is an integer.

    Returns:
        List[int]: A list of numbers (1-9) that appear exactly 9 times on the board.
    """
    count = {num: 0 for num in range(1, 10)}  # Initialize count for numbers 1-9

    # Iterate through the board and count occurrences of each number
    for row in board:
        for cell in row:
            if cell in count:
                count[cell] += 1  # Count occurrences of each number

    # Find numbers that appear exactly 9 times
    populated_numbers = [num for num, freq in count.items() if freq == 9]
    return populated_numbers
