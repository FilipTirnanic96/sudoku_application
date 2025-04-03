from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import QLineEdit, QSizePolicy


class SudokuCell(QLineEdit):
    def __init__(self, row, col, parent=None):
        super().__init__()
        self.parent = parent
        self.row = row
        self.col = col
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMaxLength(1)  # Limit input to one character

    def mousePressEvent(self, event):
        # When a cell is clicked, highlight relevant cells
        self.parent.highlight_cells(self)
        super().mousePressEvent(event)


class SudokuTimer:
    def __init__(self, parent=None):
        # Ensure 'timerLabel' exists in your UI file
        self.parent = parent
        self.game_time = QTime(0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def update_timer(self):
        """Updates the QLabel timer"""
        self.game_time = self.game_time.addSecs(1)  # Add 1 second
        if self.parent and self.parent.timerLabel:
            self.parent.timerLabel.setText(f"Time: {self.game_time.toString('mm:ss')}")  # Update UI

    def reset_timer(self):
        """Reset the timer to 0 and restart it."""
        self.timer.stop()  # Stop the timer
        self.game_time = QTime(0, 0)  # Reset elapsed time
        if self.parent and self.parent.timerLabel:
            self.parent.timerLabel.setText(f"Time: {self.game_time.toString('mm:ss')}")  # Reset display
        self.timer.start(1000)  # Restart timer every second

    def stop_timer(self):
        self.timer.stop()
