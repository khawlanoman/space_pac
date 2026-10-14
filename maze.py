from mazegenerator import MazeGenerator
from src_back.maze_loader import loader
from src_back import parsing
from src_back.game import constants
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status,Directions
import argparse


def parser_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("input", default="config.json")

    args = parser.parse_args()

    return args


def print_maze(maze:list, place_pacgum:set,corner_position:list,player_position,ghosts_place,super_pacgums,game_state) -> None:
            grid = maze
            height = len(grid)
            width = len(grid[0])

        
            print("+" + "---+" * width)

            for y in range(height):

                line = "|"

                for x in range(width):
                    if (x,y) ==  player_position:
                        cell = " @ "
                    
                    elif (x,y) == (game_state.player.x,game_state.player.y):
                        cell = " h "
            
                    elif (x,y) in ghosts_place:
                        cell = " G "
                    elif (x,y) in place_pacgum:
                        cell = " . "
                    elif (x,y) in super_pacgums:
                        cell = " & "
                    else:
                        cell = "   "


                    if grid[y][x] & 2:
                        line += cell + "|"
                    else:
                        line += cell + " "

                print(line)

                line = "+"

                for x in range(width):
                    if grid[y][x] & 4:
                        line += "---+"
                    else:
                        line += "   +"

                print(line)

def main():
    try:

        config_data = parser_args()

        data = parsing.pars_config(config_data.input)
        level= data.levels[0]
        width = level.width
        height = level.height
        seed = data.seed
        maze = loader.load_maze(width,height,seed)

        # neighbors = loader.get_valid_neighbors(maze,5,5 )
        
        player_position = loader.get_center_position(width, height)

        corner_position = loader.get_corner_positions(width, height)

        super_pacgums = loader.place_super_pacgums(width, height)
        ghosts_place = loader.place_ghosts(width, height)
        place_pacgum= loader.place_pacgums(maze, data.pacgum, corner_position, data.seed)


        count = 0
        for row in maze:
            for cell in row:
                if cell == 15:
                    count+=1

        

        count_levels = len(data.levels)



        game_state =  Game_state(maze, width, height, place_pacgum, super_pacgums, (player_position),
                                ghosts_place,0,count_levels, data.level_max_time,Game_status.PLAYING,
                                False,{},data,[])


        game_state.initialize_level()

       
        
       
        #  take data for this function 
        all_data  = game_state.all_data_to_dict()
        #  /////
        player = (all_data["player"]["x"],all_data["player"]["y"])
        # game_state.handle_input("up")
       


        game_state.handle_input("up")

        print("→", game_state.player.next_direction)
       
        print("Dictionary x:", all_data["player"]["x"])
        print("Dictionary y:", all_data["player"]["y"])

        game_state.move_player(3)

        print("Player object x:", game_state.player.x)
        print("Player object y:", game_state.player.y)
        game_state.move_player(3)

        print("pacgums:",len(game_state.pacgums))
        game_state.check_pacgum_at_player()
        print("pacgums:",len(game_state.pacgums))
        print_maze(all_data["maze"],all_data["pacgums"],all_data["super_pacgums"],player,ghosts_place, super_pacgums,game_state)

      
        

        # print(" before timer:",all_data["timer"])
        # print(" before is power:",all_data["player"]["is_power"])
        # print(" before power_time:",all_data["player"]["power_time"])

        # game_state.update_timers(10.5)
        # all_data  = game_state.all_data_to_dict()
        # print("timer:",all_data["timer"])
        # print("is power:",all_data["player"]["is_power"])
        # print("power_time:",all_data["player"]["power_time"])
        # # print(all_data["player"]["next_direction"])

    except Exception as er:
        print("ERROR:", er)

if __name__== "__main__":
    main()