# This is a sample Python script.
import sys

from PyQt5.QtWidgets import QApplication

from app_controls.control_main_window import SudokuGame


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Main function to run the app
def main():
    app = QApplication(sys.argv)  # Create the application
    window = SudokuGame()          # Create the Sudoku game window
    window.show()                  # Show the window
    sys.exit(app.exec())           # Start the application's event loop


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
