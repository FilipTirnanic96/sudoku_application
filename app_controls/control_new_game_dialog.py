from PyQt5.QtWidgets import QMainWindow, QApplication

from app_design.new_game_dialog import Ui_NewGame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app_controls.control_main_window import SudokuGame


class NewGameDialog(QMainWindow, Ui_NewGame):
    """
    Represents the New Game dialog window where the user can choose the difficulty level.
    """

    def __init__(self, parent: "SudokuGame" = None) -> None:
        """
        Initialize the New Game dialog and set up event handlers.

        Args:
            parent (SudokuGame | None): Reference to the main game window.
        """
        super(NewGameDialog, self).__init__(parent)
        self.parent = parent

        # Setup UI components
        self.setupUi(self)
        self.__setup_events()

    def __setup_events(self) -> None:
        """
        Connects buttons to their respective event handlers.
        """
        self.pushButton_Exit.clicked.connect(self.close_game)
        self.pushButton_Easy.clicked.connect(lambda: self.start_new_game(43))  # Easy: 43 empty cells
        self.pushButton_Medium.clicked.connect(lambda: self.start_new_game(46))  # Medium: 46 empty cells
        self.pushButton_Hard.clicked.connect(lambda: self.start_new_game(51))  # Hard: 51 empty cells

    def start_new_game(self, num_empty_cells: int):
        """
        Starts a new Sudoku game with the chosen difficulty.

        Args:
            num_empty_cells (int): Number of empty cells in the new Sudoku puzzle.
        """
        self.parent.process_new_game(num_empty_cells)  # Generate a new Sudoku board
        self.parent.enable_grid()  # Enable user interaction with the grid
        self.close()  # Close the New Game dialog

    def close_game(self) -> None:
        """
        Exits the application when the 'Exit' button is clicked.
        """
        QApplication.quit()
