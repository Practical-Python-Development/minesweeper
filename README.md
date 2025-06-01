# minesweeper

This is an example project go showcase pygame by building a
minesweeper clone.

## Installation
```bash
git clone https://github.com/Practical-Python-Development/minesweeper.git
cd minesweeper
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt   # requirements.txt contains: pygame
```

## Project steps:
- [x] create venv and dependency management
- [x] initialize pygame window
- [x] create a `Cell` class to represent a single tile
- [x] create mouse interaction 
- [x] build `Board` class to hold the cells
- [x] build game logic
- [ ] update rendering
- [x] add end game screen
- [ ] reinit if initial cell is mine
- [ ] restart game in end screen
- [ ] color of text dependent of number of neighbours
- [ ] add time and leaderboard