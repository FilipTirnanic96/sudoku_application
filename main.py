# This is a sample Python script.
import sys

from PyQt5.QtWidgets import QApplication

from app_controls.control_main_window import SudokuGame


# Main function to run the app
def main():
    app = QApplication(sys.argv)   # Create the application
    window = SudokuGame()          # Create the Sudoku game window
    window.show()                  # Show the window
    sys.exit(app.exec())           # Start the application's event loop


if __name__ == '__main__':
    main()
