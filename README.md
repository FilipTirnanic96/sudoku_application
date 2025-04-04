
# Sudoku Game Application

This is a simple Sudoku game built using Python and PyQt5. The application allows users to play Sudoku puzzles, providing features such as:

- **Sudoku Puzzle Generation**: Randomized puzzles with a unique solution.
- **Cell Highlighting**: Custom colors to highlight selected cells.
- **Error Handling**: Alerts and messages for invalid moves or when the player loses.
- **Timer**: Tracks time taken to solve the puzzle.
- **Interactive Interface**: A grid-based interface using PyQt5.

## Features

- **Sudoku Solver**: Automatically solves the Sudoku puzzle using backtracking.
- **User Interface**: A graphical user interface (GUI) built with PyQt5 that mimics a traditional Sudoku board.
- **Input Validation**: Ensures that the user inputs valid numbers in the Sudoku grid.
- **Game Over & Win Notifications**: Provides feedback when the player wins or loses.
- **Undo/Redo Actions**: (Optional) Can be implemented for a better user experience.

## Requirements

- Python 3.x
- PyQt5

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/sudoku-game.git
   ```

2. Navigate to the project directory:

   ```bash
   cd sudoku-game
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. The Sudoku grid will be displayed with pre-filled numbers and empty cells.
3. Click on the empty cells to input numbers (1-9).
4. Once the puzzle is solved, the timer will stop, and a congratulatory message will appear.

### Game Over:
- If the player makes three incorrect moves, a "Game Over" message will be shown.

### Sudoku Solver:
- The application can automatically solve a Sudoku puzzle using a backtracking algorithm.

## Application Flow

1. **Start a New Game**: A new randomized Sudoku puzzle is generated each time the application is run.
2. **Solve Puzzle**: The user can either solve the puzzle manually or use the solver feature.
3. **Game Over**: After three mistakes, the user loses and a message is shown.
4. **Puzzle Solved**: When the puzzle is completed correctly, a congratulatory message will appear with the time taken.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Sudoku puzzle generation and solving algorithm is based on the backtracking technique.
- PyQt5 is used for the graphical user interface.
