# Cat and Mouse Maze Game

This is a Python game where you control a mouse that must reach the cheese before being caught by the cat. The game takes place in a randomly generated maze, inspired by classic games like Pac-Man. The cat is controlled by an AI that uses the A* pathfinding algorithm to chase the mouse.

## Features
- Random maze generation using recursive backtracking (with always-closed borders)
- Cheese always placed on the secondary diagonal and accessible by path
- Smooth and continuous movement for both the mouse (player) and the cat (AI)
- Countdown before the game starts
- End screen with result and easy restart

## Algorithms Used
- **Maze Generation:** Recursive Backtracking algorithm, ensuring all paths are accessible and the borders are always walls.
- **Pathfinding:** The cat uses the A* (A-star) algorithm to find the shortest path to the mouse in real time.

## Controls
- **Arrow keys:** Move the mouse
- **Space bar:** Restart the game after it ends

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone or Download the Repository

```
git clone <repository-url>
cd <project-folder>
```

### 2. Install Dependencies

#### On Linux
```
pip3 install -r requirements.txt
```

#### On Windows
```
pip install -r requirements.txt
```

### 3. Run the Game

#### On Linux
```
python3 main.py
```

#### On Windows
```
python main.py
```

## Enjoy the game! 