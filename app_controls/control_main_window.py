import string
from typing import List

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

    def __init__(self, parent=None):
        super(SudokuGame, self).__init__(parent)
        self.parent = parent

        # setup UI
        self.setupUi(self)
        self.label_num_names = ['num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9']
        # Init internal solved and current board
        self.solved_board = [[0 for _ in range(9)] for _ in range(9)]
        self.curr_board = [[0 for _ in range(9)] for _ in range(9)]
        self.populated_numbers = []
        self.__setup_sudoku_grid()
        # Init timer
        self.game_time = None
        self.timer = SudokuTimer(self)

        # Init events
        self.__setup_events()

        # Show the New Game window immediately on startup
        self.new_game_window = NewGameDialog(self)
        self.new_game_window.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint & ~Qt.WindowMinMaxButtonsHint)
        self.show_new_game_dialog()

        # Setup mistake count value
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

        self.board: List[List[QWidget]] = []  # Store references to all QLineEdit widgets
        for row in range(9):
            row_board : List[QWidget] = []  # Store references to all QLineEdit widgets
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

    def __setup_events(self):
        """Add the event handlers."""
        # Add cell Events
        for row in range(9):
            for col in range(9):
                # connect the function when pressed Enter
                self.board[row][col].textChanged.connect(self.process_cell_input)

        # Add New game Event
        self.pushButton.pressed.connect(self.show_new_game_dialog)

    def increase_mistake_count(self):
        """Increase mistake count and update QLabel"""
        self.mistake_count += 1
        self.mistakeLabel.setText(f"Mistakes: {self.mistake_count}/3 ")
        # If mistakes reach 3, show message and disable the game
        if self.mistake_count >= 3:
            self.show_new_game_dialog()
            show_failure_message()

    def reset_mistake_count(self):
        """Reset mistake count"""
        self.mistake_count = 0
        self.mistakeLabel.setText(f"Mistakes: {self.mistake_count}/3 ")

    def highlight_cells(self, clicked_cell=None):
        """Highlight affected cells."""
        reset_cell_color_style(self.board)

        # Find row and column of clicked cell
        # Find rows and columns of the cell with the same value
        value_positions = []
        row, col = None, None
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == clicked_cell:
                    row, col = r, c
                else:
                    if (clicked_cell.text() != '') and (self.board[r][c].text() == clicked_cell.text()):
                        value_positions.append((r, c))

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

        # Highlight cells with the same value
        for (r, c) in value_positions:
            update_cell_color_style(self.board[r][c], "#87CEFA")

        # clicked cell
        update_cell_color_style(self.board[row][col], "lightblue")

    def set_board_value(self, value: int, row: int, col: int):
        """Set the board cell value."""
        self.curr_board[row][col] = value
        self.board[row][col].setText("" if value == 0 else str(value))

    def reset_board(self):
        """Reset the board values."""
        for row in range(9):
            for col in range(9):
                self.solved_board[row][col] = 0
                self.curr_board[row][col] = 0
                self.board[row][col].setText("")

    def is_valid_value(self, value: int, row: int, col: int):
        """Check if the board input value is valid."""
        valid = -1
        if value in range(1, 10):
            if value in self.populated_numbers:
                valid = -1
            else:
                valid = 1 if self.solved_board[row][col] == value else 0
        return valid

    def disable_grid(self):
        """Disable sudoku grid."""
        self.centralwidget.setEnabled(False)

    def enable_grid(self):
        """Enable sudoku grid."""
        self.centralwidget.setEnabled(True)

    def hide_populated_numbers(self, populated_numbers: List[int]) -> None:
        """
            Hides numbers that are already fully populated in the Sudoku board
            by clearing the text of corresponding QLabel elements.

            Args:
                populated_numbers (List[int]): A set of numbers (1-9) that are fully inserted in the board.
            """
        for num in range(1, 10):
            label_num_name = self.label_num_names[num - 1]
            label = self.findChild(QLabel, label_num_name)

            if num in populated_numbers:
                label.setText('')
            else:
                if label.text() == '':
                    label.setText(str(num))

    def process_cell_input(self, new_value: string):
        """Triggered when Enter is pressed in a cell.
           Check if the entered value is valid for sudoku solution."""
        # Get cell input value
        cell = self.sender()

        if isinstance(cell, QLineEdit):
            row, col = find_cell_position(cell, self.board)

            value = int(new_value) if new_value.isdigit() else 0
            valid = self.is_valid_value(value, row, col)

            if valid == -1:
                # Not valid input
                self.set_board_value(0, row, col)
                update_cell_text_color(cell, "black")
            elif valid == 0:
                # Not correct input for sudoku solution
                update_cell_text_color(cell, "red")
                self.set_board_value(value, row, col)
                # Increase mistake value
                self.increase_mistake_count()
            elif valid == 1:
                # Correct input for sudoku solution
                self.set_board_value(value, row, col)
                update_cell_text_color(cell, "black")

            self.populated_numbers = find_populated_numbers(self.curr_board)
            self.hide_populated_numbers(self.populated_numbers)
            # Check if sudoku is solved
            if (not has_zero(self.curr_board)) and check_solution(self.curr_board, self.solved_board):
                self.show_new_game_dialog()
                elapsed_time = self.timer.game_time.toString("mm:ss")
                show_sudoku_solved_message(elapsed_time)

            if valid != -1:
                cell.clearFocus()

    def show_new_game_dialog(self):
        """Show new game dialog."""
        self.timer.stop_timer()
        self.disable_grid()
        self.new_game_window.show()

    def process_new_game(self, num_empty_cells: int):
        """Generates new sudoku game."""
        # Reset timer
        self.timer.reset_timer()
        # Reset mistake counter
        self.reset_mistake_count()
        # Reset board values
        self.reset_board()
        # Reset cell colors
        reset_cell_color_style(self.board)

        # Generate new sudoku
        self.solved_board = generate_random_base_grid()
        domains = initialize_domains(self.solved_board)
        solve_sudoku(self.solved_board, domains)
        sudoku_board = generate_new_sudoku(self.solved_board, num_empty_cells)

        # set board values
        for row in range(9):
            for col in range(9):
                self.set_board_value(sudoku_board[row][col], row, col)

        self.setFocus()
