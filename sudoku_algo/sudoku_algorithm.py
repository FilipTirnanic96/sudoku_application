import copy
import random

from typing import List


# Check if placing num in the given position is valid
def is_valid(board, row, col, num):
    # Check if placing num in board[row][col] is valid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
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


def initialize_domains(board):
    """Initialize possible values (1-9) for each empty cell."""
    domains = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] for _ in range(9)]

    # Remove invalid values based on initial board
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                domains[r][c] = []  # No values allowed (already filled)
                update_domains(domains, r, c, board[r][c])

    return domains


def update_domains(domains, row, col, num):
    """Update domains in-place and return removed values to allow restoration."""
    removed_values = {}

    for i in range(9):
        if num in domains[row][i]:
            domains[row][i].remove(num)
            removed_values.setdefault((row, i), []).append(num)

        if num in domains[i][col]:
            domains[i][col].remove(num)
            removed_values.setdefault((i, col), []).append(num)

    # Remove from 3x3 subgrid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if num in domains[i][j]:
                domains[i][j].remove(num)
                removed_values.setdefault((i, j), []).append(num)

    return removed_values  # Return removed values for easy restoration


def restore_domains(domains, removed_values):
    """Restore removed values to domains after backtracking."""
    for (r, c), values in removed_values.items():
        domains[r][c].extend(values)  # Add back removed numbers


def select_unassigned_cell(board, domains):
    """Select the next cell to fill using MRV (smallest domain first)."""
    min_domain_size = float('inf')
    selected_cell = None
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domain_size = len(domains[r][c])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    selected_cell = (r, c)
    return selected_cell


def count_solutions(board, domains, count=None):
    """Count the number of valid solutions for the current board."""
    if count is None:
        count = [0]
    if count[0] > 1:
        return  # Stop early if more than one solution found

    cell = select_unassigned_cell(board, domains)
    if cell is None:  # No empty cells left → Found a valid solution
        count[0] += 1
        return

    row, col = cell
    original_domain = domains[row][col][:]  # Save current domain state

    for num in original_domain:
        if is_valid(board, row, col, num):
            board[row][col] = num

            # Track removed domain values (in-place update)
            removed_values = update_domains(domains, row, col, num)

            count_solutions(board, domains, count)

            if len(count) > 1:
                return  # Stop if more than one solution is found

            board[row][col] = 0  # Undo move
            restore_domains(domains, removed_values)  # Restore domains


def solve_sudoku(board, domains):
    """Fills the board with a valid Sudoku solution using backtracking."""
    cell = select_unassigned_cell(board, domains)
    if not cell:
        return True

    row, col = cell
    random.shuffle(domains[row][col])  # Random order for uniqueness

    for num in domains[row][col]:
        if is_valid(board, row, col, num):
            board[row][col] = num
            removed_values = update_domains(domains, row, col, num)

            if solve_sudoku(board, domains):
                return True

            board[row][col] = 0  # Backtrack
            restore_domains(domains, removed_values)  # Restore domains after backtracking
    return False


def has_unique_solution(board):
    """Check if the board has a unique solution."""
    num_solutions = [0]
    domains = initialize_domains(board)
    count_solutions(copy.deepcopy(board), domains, num_solutions)
    return num_solutions[0] == 1  # Unique if exactly one solution


MAX_NUM_TRIALS = 70


# Generate a random valid Sudoku puzzle
def generate_new_sudoku(solved_board: List[List], num_empty_cells: int):
    # Remove numbers to create the puzzle
    # You can remove a certain percentage of the numbers (e.g., 40% of them)
    board = copy.deepcopy(solved_board)
    cells_to_remove = num_empty_cells  # Total number of cells in the Sudoku grid
    num_trials = 0
    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            original_value = board[row][col]
            board[row][col] = 0
            cells_to_remove -= 1
            # Check if the board still has a unique solution
            if not has_unique_solution(board):
                board[row][col] = original_value  # Restore if it doesn't have a unique solution
                cells_to_remove += 1

            num_trials += 1
            if num_trials >= MAX_NUM_TRIALS:
                cells_to_remove = 0

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


