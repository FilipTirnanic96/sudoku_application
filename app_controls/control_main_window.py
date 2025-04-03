import string

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QGridLayout

from app_controls.control_new_game_dialog import NewGameDialog
from app_controls.model import SudokuCell, SudokuTimer
from app_controls.utility import update_cell_color_style, update_cell_text_color, find_cell_position, \
    show_failure_message, show_sudoku_solved_message, has_zero, reset_cell_color_style
from app_design.main_window import Ui_MainWindow
from sudoku_algo.sudoku_algorithm import new_sudoku_from_solved_board, check_solution, solve_sudoku, \
    generate_random_base_grid


class SudokuGame(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(SudokuGame, self).__init__(parent)
        self.parent = parent

        # setup UI
        self.setupUi(self)

        # Init internal solved and current board
        self.solved_board = [[0 for _ in range(9)] for _ in range(9)]
        self.curr_board = [[0 for _ in range(9)] for _ in range(9)]
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

    def __setup_sudoku_grid(self):
        """Initialize sudoku board."""
        # Set up main widget and layout
        self.grid_layout = QGridLayout()  # 9x9 grid layout
        self.grid_layout.setSpacing(0)

        # Create a 9x9 grid of QLineEdit widgets
        self.board = []  # Store references to all QLineEdit widgets
        for row in range(9):
            row_board = []
            for col in range(9):
                cell = SudokuCell(row, col, self)

                # ✅ Apply border styling (thicker for 3x3 Sudoku boxes)
                border_style = "1px solid gray"  # Default thin border
                if row % 3 == 0:  # Thicker top border
                    border_style += "; border-top: 3px solid black"
                if col % 3 == 0:  # Thicker left border
                    border_style += "; border-left: 3px solid black"
                if row == 8:  # Thicker bottom border
                    border_style += "; border-bottom: 3px solid black"
                if col == 8:  # Thicker right border
                    border_style += "; border-right: 3px solid black"

                cell.setStyleSheet(f"border: {border_style}; font-size: 20px;")  # Apply styling
                self.grid_layout.addWidget(cell, row, col)
                row_board.append(cell)

            self.board.append(row_board)  # Store row of board

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
        self.actionNewGame.triggered.connect(self.new_game_action)

    def increase_mistake_count(self):
        """Increase mistake count and update QLabel"""
        self.mistake_count += 1
        self.mistakeLabel.setText(f"Mistakes: {self.mistake_count}/3 ")
        # If mistakes reach 3, show message and disable the game
        if self.mistake_count >= 3:
            self.timer.stop_timer()
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
        row, col = None, None
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == clicked_cell:
                    row, col = r, c
                    break
            if row is not None:
                break

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
            valid = 1 if self.solved_board[row][col] == value else 0
        return valid

    def disable_grid(self):
        """Disable sudoku grid."""
        self.centralwidget.setEnabled(False)

    def enable_grid(self):
        """Enable sudoku grid."""
        self.centralwidget.setEnabled(True)

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
                cell.setText("")
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

            # Check if sudoku is solved
            if (not has_zero(self.curr_board)) and check_solution(self.curr_board, self.solved_board):
                self.show_new_game_dialog()
                self.timer.stop_timer()
                elapsed_time = self.timer.game_time.toString("mm:ss")
                show_sudoku_solved_message(elapsed_time)

            if valid != -1:
                cell.clearFocus()

    def new_game_action(self):
        """Shows new game dialog."""
        self.timer.stop_timer()
        self.new_game_window.show()
        self.disable_grid()

    def show_new_game_dialog(self):
        """Show new game dialog."""
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
        solve_sudoku(self.solved_board)
        sudoku_board = new_sudoku_from_solved_board(self.solved_board, num_empty_cells)

        # set board values
        for row in range(9):
            for col in range(9):
                self.set_board_value(sudoku_board[row][col], row, col)

        self.setFocus()
