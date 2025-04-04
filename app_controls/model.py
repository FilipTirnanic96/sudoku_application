from typing import Optional

from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLineEdit, QSizePolicy

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app_controls.control_main_window import SudokuGame


class SudokuCell(QLineEdit):
    """
    Represents a single cell in the Sudoku grid.

    This class extends QTableWidgetItem to customize behavior for Sudoku gameplay.
    It manages cell properties such as immutability for predefined numbers and
    highlights for user interaction.

    Features:
    - Differentiates between fixed and editable cells.
    - Changes appearance based on cell type (e.g., bold text for fixed numbers).
    - Can be selected, edited, and reset as needed.
    """

    def __init__(self, row: int, col: int, parent: Optional["SudokuGame"]=None) -> None:
        """
        Initializes a Sudoku cell, which is a specialized QLineEdit input field.

        Args:
            row (int): The row index of the cell in the Sudoku grid.
            col (int): The column index of the cell in the Sudoku grid.
            parent: Reference to the parent Sudoku game instance.
        """
        super().__init__()
        self.parent = parent  # Store reference to the parent game
        self.row = row  # Row index of the cell
        self.col = col  # Column index of the cell
        self.setAlignment(Qt.AlignCenter)  # Center the text inside the cell
        # Allow the cell to expand to fit its container
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Limit input to a single character (only one digit allowed)
        self.setMaxLength(1)

    def mousePressEvent(self, event: QMouseEvent):
        """
        Handles the mouse press event on the Sudoku cell.

        - Calls the parent's `highlight_cells` method to highlight related cells.
        - Passes the event to the base class `mousePressEvent` to handle default behavior.

        Args:
            event (QMouseEvent): The mouse click event object.
        """
        if self.parent:
            self.parent.highlight_cells(self)  # Highlight affected cells
        super().mousePressEvent(event)  # Call parent class event handler


class SudokuTimer:
    """
    A background timer for tracking the elapsed time in a Sudoku game.

    This class provides a simple timer that runs in a separate thread to keep track
    of the game's duration without blocking the main UI thread. It emits a signal
    every second to update the displayed time.

    Features:
    - Runs in a separate thread to avoid UI freezing.
    - Emits a signal every second with the updated time in HH:MM:SS format.
    - Can be started, paused, and reset as needed.
    """

    def __init__(self, parent: Optional["SudokuGame"] = None) -> None:
        """
        Initializes the Sudoku game timer.

        Args:
            parent (Optional[SudokuGame]): The parent Sudoku game instance.
        """
        self.parent = parent  # Reference to the parent game window
        self.game_time = QTime(0, 0)  # Initialize time at 00:00 (min:sec)
        self.timer = QTimer()  # Create a QTimer instance
        # Connect the timer's timeout signal to the update function
        self.timer.timeout.connect(self.update_timer)

    def update_timer(self):
        """
        Updates the timer label in the UI every second.

        - Increments the time by one second.
        - Updates the displayed time in the game's UI.
        """
        self.game_time = self.game_time.addSecs(1)  # Increment time by 1 second
        if self.parent and self.parent.timerLabel:
            self.parent.timerLabel.setText(f"Time: {self.game_time.toString('mm:ss')}")  # Update UI timer

    def reset_timer(self) -> None:
        """
        Resets the timer to 00:00 and starts it again.
        """
        self.timer.stop()  # Stop the current timer
        self.game_time = QTime(0, 0)  # Reset elapsed time to 00:00
        if self.parent and self.parent.timerLabel:
            self.parent.timerLabel.setText(f"Time: {self.game_time.toString('mm:ss')}")  # Reset displayed time
        self.timer.start(1000)  # Restart the timer with a 1-second interval

    def stop_timer(self) -> None:
        """
        Stops the timer.
        """
        self.timer.stop()
