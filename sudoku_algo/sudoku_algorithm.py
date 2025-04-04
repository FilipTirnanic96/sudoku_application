import copy
import random

from typing import List, Dict, Tuple, Optional


# Check if placing num in the given position is valid
def is_valid(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """
    Check if placing `num` in board[row][col] is valid.

    Args:
        board (List[List[int]]): The 9x9 Sudoku board.
        row (int): Row index.
        col (int): Column index.
        num (int): Number to place.

    Returns:
        bool: True if valid, False otherwise.
    """
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


def generate_random_base_grid() -> List[List[int]]:
    """
    Generate a randomized valid base Sudoku grid.

    This function creates a 9x9 Sudoku grid with only the first row filled
    with numbers 1-9 in random order. The remaining cells are set to 0.

    Returns:
        List[List[int]]: A 9x9 grid where the first row contains shuffled numbers 1-9,
                         and the rest of the grid is empty (filled with zeros).
    """
    base = list(range(1, 10))  # Create a list of numbers 1-9
    random.shuffle(base)  # Shuffle numbers to avoid fixed positions

    # Initialize a 9x9 grid filled with zeros
    grid = [[0] * 9 for _ in range(9)]

    # Assign the shuffled numbers to the first row
    grid[0] = base

    return grid


def initialize_domains(board: List[List[int]]) -> List[List[List[int]]]:
    """
   Initialize possible values (1-9) for each empty cell based on the initial board configuration.

   For each empty cell (value 0), the possible values are 1-9. Once a cell is filled (non-zero),
   the function removes invalid values from the domains (based on Sudoku rules).

   Args:
       board (List[List[int]]): A 9x9 Sudoku grid where some cells are filled and others are empty.

   Returns:
       List[List[List[int]]]: A 9x9 grid, where each cell contains a list of possible values (1-9).
                              Cells that are filled (non-zero) will have an empty list.
    """
    # Initialize the domain for each cell as 1-9
    domains = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] for _ in range(9)]

    # Remove invalid values based on initial board
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                domains[r][c] = []  # No values allowed (already filled)
                update_domains(domains, r, c, board[r][c])  # Update related cells' domains

    return domains


def update_domains(domains: List[List[List[int]]], row: int, col: int, num: int) -> Dict[Tuple[int, int], List[int]]:
    """
    Update the domains of cells in the same row, column, and 3x3 subgrid after placing a number in a cell.

    Args:
        domains (List[List[List[int]]]): A 9x9 grid of possible values for each cell.
        row (int): Row index of the cell where the number is placed.
        col (int): Column index of the cell where the number is placed.
        num (int): The number placed in the cell.

    Returns:
        Dict[Tuple[int, int], List[int]]: A dictionary where keys are coordinates of cells,
                                           and values are lists of numbers removed from the domains.
    """
    removed_values = {}

    # Remove the number from the row and column
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


def restore_domains(domains: List[List[List[int]]], removed_values: Dict[Tuple[int, int], List[int]]):
    """
    Restore the removed values back into the domains after backtracking.

    Args:
        domains (List[List[List[int]]]): A 9x9 grid of possible values for each cell.
        removed_values (Dict[Tuple[int, int], List[int]]): A dictionary where keys are coordinates of cells
                                                           and values are the removed numbers to restore.

    """
    for (r, c), values in removed_values.items():
        domains[r][c].extend(values)  # Add back removed numbers


def select_unassigned_cell(board: List[List[int]], domains: List[List[List[int]]]) -> Optional[Tuple[int, int]]:
    """
    Select the next cell to fill using MRV (Minimum Remaining Values) heuristic.
    This heuristic chooses the cell with the smallest domain (fewest possible values).

    Args:
        board (List[List[int]]): A 9x9 Sudoku grid where each cell contains an integer (0 for empty).
        domains (List[List[List[int]]]): A 9x9 grid, where each cell contains a list of possible values (1-9).

    Returns:
        Optional[Tuple[int, int]]: The coordinates of the next unassigned cell (row, col), or None if all cells are assigned.
    """
    min_domain_size = float('inf')
    selected_cell = None

    # Traverse all cells in the board to find the cell with the smallest domain
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:  # Look for unassigned cells
                domain_size = len(domains[r][c])
                if domain_size < min_domain_size:
                    min_domain_size = domain_size
                    selected_cell = (r, c)

    return selected_cell


def count_solutions(board: List[List[int]], domains: List[List[List[int]]], count: Optional[List[int]] = None) -> None:
    """
    Count the number of valid solutions for the current Sudoku board using backtracking.
    It terminates early if more than one solution is found.

    Args:
        board (List[List[int]]): A 9x9 Sudoku grid where each cell contains an integer (0 for empty).
        domains (List[List[List[int]]]): A 9x9 grid of possible values (1-9) for each empty cell.
        count (Optional[List[int]]): A list to store the count of solutions (default is [0]).

    Returns:
        None: This function modifies the `count` list in-place.
    """
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


def solve_sudoku(board: List[List[int]], domains: List[List[List[int]]]) -> bool:
    """
   Solve the Sudoku puzzle using backtracking and domain propagation.

   Args:
       board (List[List[int]]): A 9x9 Sudoku grid where each cell contains an integer (0 for empty).
       domains (List[List[List[int]]]): A 9x9 grid of possible values (1-9) for each empty cell.

   Returns:
       bool: True if a solution is found, False if no solution exists.
    """
    cell = select_unassigned_cell(board, domains)
    if not cell:
        return True  # All cells are assigned, puzzle is solved

    row, col = cell
    random.shuffle(domains[row][col])  # Random order for uniqueness

    # Try each number in the cell's domain
    for num in domains[row][col]:
        if is_valid(board, row, col, num):
            board[row][col] = num
            removed_values = update_domains(domains, row, col, num)

            # Recursively try to solve the board
            if solve_sudoku(board, domains):
                return True

            board[row][col] = 0  # Backtrack
            restore_domains(domains, removed_values)  # Restore domains after backtracking

    return False  # No solution found, return False


def has_unique_solution(board: List[List[int]]) -> bool:
    """
    Check if the Sudoku board has a unique solution.

    This function uses the count_solutions method to check if there is exactly one valid solution for the given board.

    Args:
        board (List[List[int]]): A 9x9 Sudoku grid where each cell contains an integer (0 for empty).

    Returns:
        bool: True if the board has exactly one solution, False otherwise.
    """
    num_solutions = [0]
    domains = initialize_domains(board)  # Initialize domains for empty cells
    count_solutions(copy.deepcopy(board), domains, num_solutions)  # Count solutions using backtracking
    return num_solutions[0] == 1  # Unique if exactly one solution


MAX_NUM_TRIALS = 60  # Maximum number of trials before giving up on finding a valid puzzle


# Generate a random valid Sudoku puzzle
def generate_new_sudoku(solved_board: List[List], num_empty_cells: int):
    """
    Generate a new Sudoku puzzle by removing numbers from a solved board while ensuring it has a unique solution.

    Args:
        solved_board (List[List[int]]): A fully solved Sudoku board.
        num_empty_cells (int): The number of cells to be emptied in the puzzle to create difficulty.

    Returns:
        List[List[int]]: A Sudoku board with some cells emptied, having a unique solution.
    """
    # Make a deep copy of the solved board to avoid modifying the original
    board = copy.deepcopy(solved_board)
    cells_to_remove = num_empty_cells  # Total number of cells to remove
    num_trials = 0  # Counter for the number of trials to generate a valid puzzle

    while cells_to_remove > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)  # Randomly select a cell
        if board[row][col] != 0:   # Only remove if the cell is not already empty
            original_value = board[row][col]
            board[row][col] = 0   # Remove the number from the cell
            cells_to_remove -= 1

            # Check if the board still has a unique solution
            if not has_unique_solution(board):
                board[row][col] = original_value  # Restore if it doesn't have a unique solution
                cells_to_remove += 1  # Undo the removal

            num_trials += 1
            if num_trials >= MAX_NUM_TRIALS:  # Stop if too many trials are made
                cells_to_remove = 0  # Terminate puzzle creation

    return board


def check_solution(board: List[List[int]], solved_board: List[List[int]]) -> bool:
    """
    Check if the provided board is identical to the solved board.

    Args:
        board (List[List[int]]): A Sudoku grid representing the user's solution.
        solved_board (List[List[int]]): A fully solved Sudoku board.

    Returns:
        bool: True if the provided board matches the solved board, False otherwise.
    """
    ret_val = True
    for row in range(9):
        for col in range(9):
            if board[row][col] != solved_board[row][col]:  # Check for any mismatch
                ret_val = False  # Return False if any mismatch is found
                break
        if not ret_val:
            break

    return ret_val


