import copy
import random

from typing import List


# Check if placing num in the given position is valid
def is_valid(board, row, col, num):
    # Check the row
    if num in board[row]:
        return False

    # Check the column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def generate_random_base_grid():
    """Generate a randomized valid Sudoku grid to start from."""
    base = list(range(1, 10))
    random.shuffle(base)  # Shuffle numbers to avoid fixed positions

    grid = [[0] * 9 for _ in range(9)]

    # Fill the first row with shuffled numbers
    grid[0] = base

    return grid

# Solve Sudoku using backtracking
def solve_sudoku(board: List[List]):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


# Generate a random valid Sudoku puzzle
def new_sudoku_from_solved_board(solved_board: List[List], num_empty_cells: int) -> List[List]:
    # Remove numbers to create the puzzle
    # You can remove a certain percentage of the numbers (e.g., 40% of them)
    board = copy.deepcopy(solved_board)
    attempts = num_empty_cells  # Total number of cells in the Sudoku grid
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            backup = board[row][col]
            board[row][col] = 0
            # You can implement a checking function here to ensure the puzzle has one unique solution
            attempts -= 1

    return board


def check_solution(board, solved_board):
    ret_val = True
    for row in range(9):
        for col in range(9):
            if board[row][col] != solved_board[row][col]:
                ret_val = False
                break
        if not ret_val:
            break

    return ret_val

