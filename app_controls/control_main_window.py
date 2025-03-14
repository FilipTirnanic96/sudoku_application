from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QGridLayout, QSizePolicy

from app_design.main_window_ui import Ui_MainWindow


class SudokuGame(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(SudokuGame, self).__init__(parent)
        self.parent = parent

        # setup UI
        self.setupUi(self)
        self.__setup_sudoku_grid()

    def __setup_sudoku_grid(self):
        # Set up main widget and layout
        self.grid_layout = QGridLayout()  # 9x9 grid layout
        self.grid_layout.setSpacing(0)

        # Create a 9x9 grid of QLineEdit widgets
        self.cells = []  # Store references to all QLineEdit widgets
        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = QLineEdit()
                cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text
                cell.setMaxLength(1)  # Limit input to one character

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

                # connect the function when pressed Enter
                cell.returnPressed.connect(lambda r=row, c=col: self.process_cell_input(r, c)) # Connect Enter key event

                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)

            self.cells.append(row_cells)  # Store row of cells

        # Apply layout to main widget
        self.centralwidget.setLayout(self.grid_layout)

        # Adjust grid layout row and column stretching
        for row in range(9):
            self.grid_layout.setRowStretch(row, 1)  # Allow rows to stretch equally
        for col in range(9):
            self.grid_layout.setColumnStretch(col, 1)  # Allow columns to stretch equally

    def process_cell_input(self, row, col):
        """Triggered when Enter is pressed in a cell."""
        cell = self.cells[row][col]
        text = cell.text()
        cell.clearFocus()  # Remove focus (cursor disappears)

    def process_new_game(self):
        # generate new sudoku
        # remove random numbers
        # check if the sudoku solution is unique
        #
        return
