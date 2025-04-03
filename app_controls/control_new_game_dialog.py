from PyQt5.QtWidgets import QMainWindow, QApplication

from app_design.new_game_dialog import Ui_NewGame


class NewGameDialog(QMainWindow, Ui_NewGame):

    def __init__(self, parent=None):
        super(NewGameDialog, self).__init__(parent)
        self.parent = parent

        # setup UI
        self.setupUi(self)
        self.__setup_events()

    def __setup_events(self):
        self.pushButton_Exit.clicked.connect(self.close_game)
        self.pushButton_Easy.clicked.connect(lambda: self.start_new_game(43))
        self.pushButton_Medium.clicked.connect(lambda: self.start_new_game(50))
        self.pushButton_Hard.clicked.connect(lambda: self.start_new_game(57))

    def start_new_game(self, num_empty_cells: int):
        """Restart the Sudoku game."""
        self.parent.process_new_game(num_empty_cells)
        self.parent.enable_grid()
        self.close()  # Close this dialog

    def close_game(self):
        """Exit the application."""
        QApplication.quit()
