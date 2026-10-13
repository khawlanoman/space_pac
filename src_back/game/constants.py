from enum import Enum


class Directions(Enum):
    UP = (0,-1, 1)
    DOWN = (0, 1, 4)
    LEFT = (-1, 0, 8)
    RIGHT = (1, 0, 2)


class Opposite(Enum):
    UP = "DOWN"
    DOWN = "UP"
    LEFT = "RGIHT"
    RIGHT  = "LEFT"


class Cell(Enum):
    WALL = 0
    WAY = 1
    PACGUM = 2
    SUPER_PACGUM = 3

class Game_status(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class Ghost_state(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"

class Ghost_type(Enum):
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"

class Defaults(Enum):
    LIVES = 3,
    PACGUM_COUNT = 42
    POINTS_PACGUM = 10
    POINTS_SUPER_PACGUM = 50
    POINTS_GHOST = 200
    PLAYER_SPEED = 5.0
    GHOST_SPEED = 4.0
    GHOST_FRIGHTENED_SPEED = 2.0
    GHOST_EATEN_SPEED = 8.0
    FRIGHTENED_DURATION = 7.0
    RESPAWN_TIME = 5.0
    INVINCIBILITY_TIME = 2.0
    LEVEL_MAX_TIME = 90.0
    MAZE_WIGHT = 15
    MAZE_HEIGHT = 15
    NUM_LEVELS = 10
    SEED = 42