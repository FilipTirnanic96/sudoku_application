
# Sudoku Game Application

This is a simple Sudoku game built using Python and PyQt5. The application allows users to play Sudoku puzzles, providing features such as:

- **Sudoku Puzzle Generation**: Randomized puzzles with a unique solution.
- **Cell Highlighting**: Custom colors to highlight selected cells.
- **Error Handling**: Alerts and messages for invalid moves or when the player loses.
- **Timer**: Tracks time taken to solve the puzzle.
- **Interactive Interface**: A grid-based interface using PyQt5.

## Features

- **Sudoku Solver**: Automatically solves the Sudoku puzzle using Optimazed Backtracking with Lookahead.
- **User Interface**: A graphical user interface (GUI) built with PyQt5 that mimics a traditional Sudoku board.
- **Game Over & Win Notifications**: Provides feedback when the player wins or loses.

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
2. Select new game with specified difficulty.
3. The Sudoku grid will be displayed with pre-filled numbers and empty cells.
4. Click on the empty cells to input numbers (1-9).
5. Once the puzzle is solved, the timer will stop, and a congratulatory message will appear.
6. If the player makes three incorrect moves, a "Game Over" message will be shown.

## Application Flow

1. **Start a New Game with selected difficulty**: A new randomized Sudoku puzzle is generated each time the new game is selected. <br/> <br/>
   <img src="https://github.com/user-attachments/assets/7c07d3b7-92c7-4627-96b6-360bfe161a6e" alt="Description" width="350" height="360">

2. **Solve Puzzle**: The user solves the puzzle manually. <br/>  <br/>
   <img src="https://github.com/user-attachments/assets/7fd6b125-4e44-483f-ad06-f35484e9c5bf" alt="Description" width="350" height="360">

3. **Game Over**: After three mistakes, the user loses and a message is shown. <br/>  <br/>
   <img src="https://github.com/user-attachments/assets/4d5924f3-abb6-436f-aed6-d25d58beb17a" alt="Description" width="350" height="360">

4. **Puzzle Solved**: When the puzzle is completed correctly, a congratulatory message will appear with the time taken. <br/>  <br/>
   <img src="https://github.com/user-attachments/assets/b38c1b5d-b397-4ebe-966b-e8f173b26d32" alt="Description" width="350" height="360">

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
