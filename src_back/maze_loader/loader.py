from mazegenerator import MazeGenerator
from src_back.game.constants import Directions
from random import Random
def load_maze( width:int,height:int,seed:int) -> list:
    grid = MazeGenerator(size=(width,height),perfect=False,seed=seed)

    return grid.maze



def has_wall(maze:list, r: int,c: int, direction:tuple)-> bool :

    cell_bit = maze[r][c]
    dire_bit = direction.value[2]
    return (cell_bit & dire_bit) != 0


def can_move(maze:list, x:int, y:int, direction:tuple)->bool:
    dire_x =direction.value[0]
    dire_y = direction.value[1]

    nx, ny = (x + dire_x, y + dire_y)

    if (nx <= 0 or nx > x) and  (ny <= 0 or ny > y):
        return False
    
    wall =has_wall(maze,0,0,direction)
    if wall == True:
        return False
    return True



def  get_valid_neighbors(maze, x: int,y :int)-> list:
    neighbors_valid = []
    for d in Directions:
        dx = d.value[0]
        dy = d.value[1]
        if can_move(maze,x ,y,d):
            neighbors_valid.append((x+dx , y+dy))
    
    return neighbors_valid


def get_center_position(width:int , height: int)-> tuple:
    center_x = width // 2
    center_y = height // 2

    return (center_x, center_y)

def get_corner_positions(width: int, height: int) -> list:
    positions = [(0,0),(width - 1, 0)
                     ,(0, height - 1)
                     ,(width - 1, height - 1)]
    
    return positions

def place_super_pacgums(width: int, height: int)-> list:
    list_place = get_corner_positions(width, height)
    return list_place


def place_ghosts(width: int, height: int)-> list:
    positions = [(1,0),(width - 2, 0)
                     ,(1, height - 1)
                     ,(width - 2, height - 1)]
    
    return positions

def place_pacgums(maze, count:int, exclude_po, seed:int) -> list:
    width = len(maze[0])
    height = len(maze)

    places= []

    for y in range(height-1) :
        for x in range(width-1):
            if maze[y][x] == 15 :
                continue
            elif (x, y) in exclude_po:
                continue
            places.append((x,y))
    if count > len(places):
        print("error pacgum number ")
        count = len(places)


    rendom_gen = Random(seed)
    rendom_gen.shuffle(places)

    pacgums  =set(places[0:count])
    return pacgums

