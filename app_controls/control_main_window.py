from typing import List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QGridLayout, QLabel, QWidget

from app_controls.control_new_game_dialog import NewGameDialog
from app_controls.model import SudokuCell, SudokuTimer
from app_controls.utility import update_cell_color_style, update_cell_text_color, find_cell_position, \
    show_failure_message, show_sudoku_solved_message, has_zero, reset_cell_color_style, find_populated_numbers
from app_design.main_window import Ui_MainWindow
from sudoku_algo.sudoku_algorithm import check_solution, solve_sudoku, \
    generate_random_base_grid, generate_new_sudoku, initialize_domains


class SudokuGame(QMainWindow, Ui_MainWindow):
    """
    A PyQt5-based Sudoku game application.

    This class implements a Sudoku game with the following features:
    - A 9x9 Sudoku grid with interactive cells (QLineEdit).
    - A game timer to track the player's solving time.
    - A mistake counter that limits incorrect entries to a maximum of 3.
    - A number selection panel that hides fully populated numbers.
    - A highlight feature that emphasizes related cells and identical numbers.
    - A validation mechanism that checks user input against the solution.
    - An option to generate a new Sudoku game with different difficulty levels.

    The game starts with a 'New Game' dialog that allows players to begin a fresh puzzle.
    Players can input numbers into the grid, and incorrect entries are highlighted.
    Upon solving the puzzle, the game displays a success message.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initializes the SudokuGame instance, sets up the user interface, initializes the game state,
        and sets up the event handlers.

        This constructor:
        - Initializes the solved and current Sudoku boards.
        - Sets up the Sudoku grid.
        - Initializes the game timer.
        - Sets up the event handlers for user interactions.
        - Displays the 'New Game' window immediately on startup.
        - Initializes the mistake count for the game.

        Args:
            parent (Optional[QWidget], optional): The parent widget, default is None.
        """
        super(SudokuGame, self).__init__(parent)   # Call parent constructor to initialize the widget
        self.parent = parent

        # Setup the user interface (UI) using a UI setup method
        self.setupUi(self)

        # Initialize a list of labels for numbers (1-9) displayed in the UI
        self.label_num_names = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9']

        # Initialize internal boards (solved and current board) with all zeros
        self.solved_board = [[0 for _ in range(9)] for _ in range(9)]  # Solved board
        self.curr_board = [[0 for _ in range(9)] for _ in range(9)]  # Current game board (modifiable by the player)

        # List to store populated numbers (those already inserted on the board)
        self.populated_numbers = []

        # Set up the Sudoku grid on the UI (calls a helper function to create and display the grid)
        self.__setup_sudoku_grid()

        # Initialize the game timer
        self.timer = SudokuTimer(self)

        # Initialize event handlers to manage user actions
        self.__setup_events()

        # Create and display the New Game window on startup (this allows the user to start a new game)
        self.new_game_window = NewGameDialog(self)
        # Customize window flags (disable close and minimize/maximize buttons)
        self.new_game_window.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMinMaxButtonsHint)
        self.show_new_game_dialog()  # Show the New Game dialog window immediately

        # Initialize the mistake counter (tracks how many mistakes the player has made)
        self.mistake_count = 0

    def __setup_sudoku_grid(self) -> None:
        """
        Initialize the Sudoku board with a 9x9 grid of QLineEdit widgets.

        This function sets up the main grid layout, creates Sudoku cells (QLineEdit),
        applies styling, and ensures proper 3x3 subgrid borders.
        """
        # Create a grid layout for the Sudoku board
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)

        self.board: List[List[QLineEdit]] = []  # Store references to all QLineEdit widgets
        for row in range(9):
            row_board: List[QLineEdit] = []  # Store references to all QLineEdit widgets
            for col in range(9):
                cell = SudokuCell(row, col, self)  # Create a cell widget

                # Define border thickness for 3x3 Sudoku boxes
                top_border = "3px solid black" if row % 3 == 0 else "1px solid gray"
                left_border = "3px solid black" if col % 3 == 0 else "1px solid gray"
                bottom_border = "3px solid black" if row == 8 else "1px solid gray"
                right_border = "3px solid black" if col == 8 else "1px solid gray"

                # Apply borders properly
                cell.setStyleSheet(
                    f"border-top: {top_border};"
                    f"border-left: {left_border};"
                    f"border-bottom: {bottom_border};"
                    f"border-right: {right_border};"
                    "font-size: 20px;"
                )

                # Add cell to grid layout at (row, col)
                self.grid_layout.addWidget(cell, row, col)
                row_board.append(cell)

            self.board.append(row_board)  # Append row to board list

        # Apply layout to main widget
        self.centralwidget.setLayout(self.grid_layout)

    def __setup_events(self) -> None:
        """
        Set up event handlers for the Sudoku board.

        This function connects input events for Sudoku cells and a button click event
        for starting a new game.
        """
        # Connect events for each Sudoku cell
        for row in range(9):
            for col in range(9):
                # Connect textChanged event to process_cell_input function
                self.board[row][col].textChanged.connect(self.process_cell_input)

        # Connect event for "New Game" button
        self.pushButton.pressed.connect(self.show_new_game_dialog)

    def increase_mistake_count(self) -> None:
        """
        Increases the mistake count and updates the QLabel displaying mistakes.

        - If the mistake count reaches 3, the game is disabled, and a failure message is shown.
        """
        self.mistake_count += 1  # Increment mistake count
        self.mistakeLabel.setText(f"Mistakes: {self.mistake_count}/3 ")  # Update mistake label

        # Check if mistake limit is reached
        if self.mistake_count >= 3:
            self.show_new_game_dialog()  # Show new game dialog
            show_failure_message()  # Display failure message

    def reset_mistake_count(self) -> None:
        """
        Resets the mistake count to 0 and updates the QLabel.
        """
        self.mistake_count = 0  # Reset count
        self.mistakeLabel.setText(f"Mistakes: {self.mistake_count}/3 ")  # Update mistake label

    def highlight_cells(self, clicked_cell: Optional[QLineEdit] = None) -> None:
        """
        Highlights relevant cells in the Sudoku grid when a cell is clicked.

        - Highlights the row, column, and 3x3 subgrid of the clicked cell.
        - Highlights other cells with the same value.
        - Resets the background of previously highlighted cells before applying new highlights.

        Args:
            clicked_cell (Optional[QLineEdit]): The cell that was clicked. Defaults to None.
        """
        # Reset colors of all cells before applying highlights
        reset_cell_color_style(self.board)

        # Find the row and column of the clicked cell, and find other cells with the same value
        value_positions = []  # Stores positions of cells with the same value
        row, col = None, None  # Initialize row and column variables
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == clicked_cell:   # Identify clicked cell's position
                    row, col = r, c
                else:
                    # If the clicked cell has a value, find all other cells with the same value
                    if clicked_cell and clicked_cell.text() and (self.board[r][c].text() == clicked_cell.text()):
                        value_positions.append((r, c))

        # Return early if no valid cell was clicked
        if row is None or col is None:
            return

        # Highlight the row and column
        for i in range(9):
            update_cell_color_style(self.board[row][i], "aliceblue")
            update_cell_color_style(self.board[i][col], "aliceblue")

        # Highlight 3x3 subgrid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                update_cell_color_style(self.board[i][j], "aliceblue")

        # Highlight cells containing the same number
        for (r, c) in value_positions:
            update_cell_color_style(self.board[r][c], "#87CEFA") # Light blue

        # Highlight the clicked cell with a distinct color
        update_cell_color_style(self.board[row][col], "lightblue")

    def set_board_value(self, value: int, row: int, col: int) -> None:
        """
        Sets the given value in the specified board cell.

        - Updates both the logical board representation and the UI.
        - If the value is 0, clears the cell in the UI.

        Args:
            value (int): The number to set in the cell (1-9, or 0 to clear).
            row (int): The row index of the cell (0-8).
            col (int): The column index of the cell (0-8).
        """
        self.curr_board[row][col] = value
        self.board[row][col].setText("" if value == 0 else str(value))

    def reset_board(self) -> None:
        """
        Resets the Sudoku board to an empty state.

        - Clears both the solution board (`solved_board`) and the current board (`curr_board`).
        - Removes all displayed numbers from the UI.
        """
        for row in range(9):
            for col in range(9):
                self.solved_board[row][col] = 0  # Reset solved board
                self.curr_board[row][col] = 0  # Reset current board
                self.board[row][col].setText("")  # Clear the UI cell

    def is_valid_value(self, value: int, row: int, col: int) -> int:
        """
        Checks if the input value is valid for the given board cell.

        - Returns -1 if the value is already placed (fixed number).
        - Returns 1 if the value is correct (matches the solution board).
        - Returns 0 if the value is incorrect.

        Args:
            value (int): The number to validate (1-9).
            row (int): The row index (0-8).
            col (int): The column index (0-8).

        Returns:
            int: -1 (invalid input), 1 (correct placement), or 0 (incorrect placement).
        """
        valid = -1
        if value in range(1, 10):
            if value in self.populated_numbers:  # If it's a fixed number, it's invalid
                valid = -1
            else:
                valid = 1 if self.solved_board[row][col] == value else 0  # Check correctness
        return valid

    def disable_grid(self):
        """
        Disables the Sudoku grid, preventing further input.

        - Disables the main widget that contains the grid.
        """
        self.centralwidget.setEnabled(False)

    def enable_grid(self):
        """
        Enables the Sudoku grid, allowing user input.

        - Re-enables the main widget that contains the grid.
        """
        self.centralwidget.setEnabled(True)

    def hide_populated_numbers(self, populated_numbers: List[int]) -> None:
        """
        Hides numbers that are already fully populated in the Sudoku board
        by clearing the text of corresponding QLabel elements.

        Args:
            populated_numbers (List[int]): A set of numbers (1-9) that are fully inserted in the board.
        """
        for num in range(1, 10):
            label_num_name = self.label_num_names[num - 1]  # Get the QLabel name
            label = self.findChild(QLabel, label_num_name)   # Find QLabel by name

            if num in populated_numbers:
                label.setText('')  # Hide fully populated number
            else:
                if label.text() == '':
                    label.setText(str(num))  # Restore number if it was cleared

    def process_cell_input(self, new_value: str) -> None:
        """
        Handles the event when a new value is entered in a Sudoku cell.

        - Validates the input against Sudoku rules.
        - Updates the board and checks if the game is solved.
        - Highlights incorrect values in red and increases mistake count.
        - Checks if the puzzle is solved and shows a success message.

        Args:
            new_value (str): The text input entered into the Sudoku cell.
        """
        # Get the cell where input occurred
        cell = self.sender()

        if isinstance(cell, QLineEdit):
            # Find row and column of the edited cell
            row, col = find_cell_position(cell, self.board)

            # Convert input value to integer (0 if invalid)
            value = int(new_value) if new_value.isdigit() else 0
            valid = self.is_valid_value(value, row, col)  # Validate the value

            if valid == -1:
                # Invalid input (not allowed in Sudoku)
                self.set_board_value(0, row, col)
                update_cell_text_color(cell, "black")
            elif valid == 0:
                # Incorrect input for Sudoku solution
                self.set_board_value(value, row, col)
                update_cell_text_color(cell, "red")
                self.highlight_cells(cell)
                self.increase_mistake_count()  # Track mistakes
            elif valid == 1:
                # Correct input
                self.set_board_value(value, row, col)
                update_cell_text_color(cell, "black")
                self.highlight_cells(cell)

            # Update populated numbers and hide them
            self.populated_numbers = find_populated_numbers(self.curr_board)
            self.hide_populated_numbers(self.populated_numbers)

            # Check if the Sudoku puzzle is solved
            if (not has_zero(self.curr_board)) and check_solution(self.curr_board, self.solved_board):
                self.show_new_game_dialog()
                elapsed_time = self.timer.game_time.toString("mm:ss")
                show_sudoku_solved_message(elapsed_time)  # Display success message

            # Remove focus from the cell after entering a valid value
            if valid != -1:
                cell.clearFocus()

    def show_new_game_dialog(self)  -> None:
        """
        Displays a dialog for starting a new Sudoku game.

        - Stops the game timer.
        - Disables the current grid to prevent further input.
        - Opens a new game selection window.
        """
        self.timer.stop_timer()
        self.disable_grid()
        self.new_game_window.show()

    def process_new_game(self, num_empty_cells: int) -> None:
        """
        Generates a new Sudoku game with a specified number of empty cells.

        - Resets the game timer and mistake count.
        - Resets the board values and cell colors.
        - Generates a new random Sudoku puzzle by solving a base grid and removing values to create empty cells.
        - Sets the values for the new puzzle on the board.

        Args:
            num_empty_cells (int): The number of empty cells that should be present in the new Sudoku puzzle.
        """
        # Reset the game timer
        self.timer.reset_timer()

        # Reset the mistake count to zero
        self.reset_mistake_count()

        # Reset all board values to their initial state (clearing the board)
        self.reset_board()

        # Reset the colors of the cells (for any highlights or color changes during the game)
        reset_cell_color_style(self.board)

        # Generate a new solved Sudoku base grid (fully solved board)
        self.solved_board = generate_random_base_grid()
        # Initialize domains (possible values) for the Sudoku grid
        domains = initialize_domains(self.solved_board)
        # Solve the generated Sudoku base grid (filling all cells)
        solve_sudoku(self.solved_board, domains)

        # Generate the new Sudoku puzzle by removing the specified number of cells
        sudoku_board = generate_new_sudoku(self.solved_board, num_empty_cells)

        # Set the values for the new puzzle on the Sudoku board
        for row in range(9):
            for col in range(9):
                self.set_board_value(sudoku_board[row][col], row, col)

        # Set focus back to the main window or widget after the new game has been set up
        self.setFocus()
