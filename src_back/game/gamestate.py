from .constants import Ghost_state, Ghost_type, Game_status,Directions
from .player import PlayerState
from .ghost import GhostState
from  ..models import Game_config
from random import randint
from ..maze_loader import loader

class Game_state:

    def __init__(self,maze:list[list[int]],width:int,height:int,pacgums:set[tuple[int,int]],
                 super_pacgums:set[tuple[int,int]],player:PlayerState,
                 ghosts:list[GhostState],score:int, level:int, timer:float,game_status:Game_status,
                 cheat_mode:bool, cheats:dict[str,bool],config:Game_config, highscores:list[dict]) -> None:

                 self.maze = maze
                 self.width = width
                 self.height = height
                 self.pacgums = pacgums
                 self.super_pacgums =super_pacgums
                 self.player = player
                 self.ghosts = ghosts
                 self.score = score
                 self.level = level
                 self.timer = timer
                 self.game_status = game_status
                 self.cheat_mode = cheat_mode
                 self.cheats = cheats
                 self.config = config
                 self.highscores = highscores

    def initialize_level(self) -> None:
        """ this function  for  initialization all the data we need  to use """
        exclude_po = []
        player_position = loader.get_center_position(self.width, self.height)

        ghosts_position = loader.place_ghosts(self.width, self.height)

        super_pacgums = loader.place_super_pacgums(self.width,self.height)

        exclude_po.extend(player_position)
        exclude_po.extend(ghosts_position)
        exclude_po.extend(super_pacgums)
        ghost_freaid = 3.0
    
        if self.level == 0:
            level_seed = self.config.seed
        else:
            level_seed = randint(1, 100)

        self.maze = loader.load_maze(self.width,self.height, level_seed)

        self.pacgums = loader.place_pacgums(self.maze,self.config.pacgum,exclude_po,level_seed)
        self.super_pacgums = loader.place_super_pacgums(self.width,self.height)

        self.player = PlayerState(player_position[0],player_position[1],
                             Directions.RIGHT,None,self.config.lives,self.score )

        blinky_ghost = GhostState(ghosts_position[0][0],ghosts_position[0][1],Directions.LEFT,
                                  Ghost_type.BLINKY,Ghost_state.SCATTER,ghosts_position[0],ghost_freaid)
        
        plinky_ghost = GhostState(ghosts_position[1][0],ghosts_position[1][1],Directions.LEFT,
                                  Ghost_type.PINKY,Ghost_state.SCATTER,ghosts_position[1],ghost_freaid)
        
        inky_ghost = GhostState(ghosts_position[2][0],ghosts_position[2][1],Directions.LEFT,
                                Ghost_type.INKY,Ghost_state.SCATTER,ghosts_position[2],ghost_freaid)
        
        clyde_ghost = GhostState(ghosts_position[3][0],ghosts_position[3][1],Directions.LEFT,
                                Ghost_type.CLYDE,Ghost_state.SCATTER,ghosts_position[3],ghost_freaid)
        
        self.ghosts = [blinky_ghost,plinky_ghost,inky_ghost,clyde_ghost]
        self.timer = self.config.level_max_time

        self.game_status = Game_status.PLAYING


    def all_data_to_dict(self) -> dict:
        """ this function is add  all data we need it  to dict """
        result_dict = {"maze":self.maze,
                       "width": self.width,
                       "height": self.height,
                       "player": self.player.player_dict(),
                       "ghosts": [ghost.ghosts_dict() for ghost in self.ghosts],
                       "pacgums": list(self.pacgums),
                       "super_pacgums":list(self.super_pacgums),
                       "score": self.score,
                       "level": self.level,
                       "timer": self.timer,
                       "game_status": self.game_status.value,
                       "cheat_mode" : self.cheat_mode,
                       "cheats": self.cheats,
                       "highscores": self.highscores}

        return result_dict


    def handle_input(self,direct:str) -> None :
        """ this function is handel the input key by convert it to enum value  """
        if direct == "up":
            self.player.next_direction = Directions.UP
        elif direct == "down":
            self.player.next_direction = Directions.DOWN
        elif direct == "left":
            self.player.next_direction = Directions.LEFT
        elif direct == "right":
            self.player.next_direction = Directions.RIGHT
    

    def update_timers(self,tm:float)-> None:
        """ this method is for count time of power of player and the time of level"""
        self.timer -= tm
        if self.timer <= 0.0:
            self.timer = 0.0
        
        if self.player.is_power:
            self.player.power_time -= tm
            if self.player.power_time <= 0.0:
                self.player.is_power= False
                self.player.power_time = 0.0
        




    def move_player(self, dt):
            """ this methode is moves the player in the current direction if there is no wall """
            tile_x = int(self.player.x)
            tile_y = int(self.player.y)
            

            if self.player.next_direction:
                if loader.can_move(self.maze, tile_x, tile_y, self.player.next_direction):
                    self.player.direction = self.player.next_direction
                    self.player.next_direction = None
  
                
 
            if not loader.can_move(self.maze, tile_x, tile_y, self.player.direction):
                return  
            
            dx, dy = self.player.direction.value[:2]
            target_x = tile_x + dx
            target_y = tile_y + dy
            
            distance = self.player.speed * dt
            
            if dx > 0:
                self.player.x = min(self.player.x + distance, target_x)
            elif dx < 0:
                self.player.x = max(self.player.x - distance, target_x)
            if dy > 0:
                self.player.y = min(self.player.y + distance, target_y)
            elif dy < 0:
                self.player.y = max(self.player.y - distance, target_y)


    def check_pacgum_at_player(self)-> None:
        """this function is check the position of pacman and super_pacgums,pacgums, 
            if pacman and one of them in the same position  remove it from the list of super_pacgums or
            pacgums and add the points to score
        """
        player_x = int(self.player.x)
        player_y = int(self.player.y)

        if (player_x,player_y) in self.pacgums:
            self.pacgums.remove((player_x,player_y))
            self.score += self.config.points_per_pacgum

        if (player_x,player_y) in self.super_pacgums:
            self.super_pacgums.remove((player_x,player_y))

            for ghost in self.ghosts:
                ghost.state =  Ghost_state.FRIGHTENED
                ghost.ghost_freaid = 20.0
            self.score += self.config.points_per_super_pacgum


    def  rest_player(self) -> None :
        """  this function is for decrement 
        player live if  not in power mode , 
        and back the player and  ghosts in ther first position """
        self.player.lives -= 1

        if self.player.lives <= 0 :
           self.game_status = Game_status.GAME_OVER
           return
        
        player_position = loader.get_center_position(self.width, self.height)
        ghosts_position = loader.place_ghosts(self.width, self.height)

        self.player.x, self.player.y = player_position

        for ghost in self.ghosts:
            if ghost.ghost_type == Ghost_type.BLINKY:
                ghost.x,ghost.y = ghosts_position[0][0], ghosts_position[0][1]
            elif ghost.ghost_type == Ghost_type.PINKY:
                ghost.x,ghost.y = ghosts_position[1][0], ghosts_position[1][1]
            elif ghost.ghost_type == Ghost_type.INKY:
                ghost.x,ghost.y = ghosts_position[2][0], ghosts_position[2][1]
            elif ghost.ghost_type == Ghost_type.CLYDE:
                ghost.x,ghost.y = ghosts_position[3][0], ghosts_position[3][1]


    def check_ghost_collision(self) -> None:
        """ this function is for check position
        of ghost  and change it state """
        player_x = int(self.player.x)
        player_y = int(self.player.y)

        for ghost in self.ghosts:

            print("lives:", self.player.lives)
            print("ghosts_state:", ghost.state)
            if (ghost.x, ghost.y) != (player_x, player_y):
                continue


            if ghost.state ==  Ghost_state.EATEN:
                continue

            elif ghost.state ==  Ghost_state.FRIGHTENED:
                ghost.state = Ghost_state.EATEN
                ghost.respawn_time = 30.0
            
            else:
                self.rest_player()
                break


    def update_ghosts_time(self, time) ->None:
        """ this function is for  update the time
        of freaid ghost and respawn time of ghost """
        for ghost in self.ghosts:
            if ghost.state == Ghost_state.FRIGHTENED:
                ghost.ghost_freaid -= time
                
                if ghost.ghost_freaid <= 0:
                    ghost.ghost_freaid = 0.0
                    ghost.state = Ghost_state.SCATTER

            if ghost.state == Ghost_state.EATEN:
                ghost.respawn_time -= time

                if ghost.respawn_time <= 0:
                    ghost.respawn_time = 0.0
                    ghost.state = Ghost_state.SCATTER

    def check_ghost(self, ghost)  -> None:
        ghosts_position = loader.place_ghosts(self.width, self.height)

        if ghost.ghost_type == Ghost_type.BLINKY:
            ghost.x,ghost.y = ghosts_position[0][0], ghosts_position[0][1]
        elif ghost.ghost_type == Ghost_type.PINKY:
            ghost.x,ghost.y = ghosts_position[1][0], ghosts_position[1][1]
        elif ghost.ghost_type == Ghost_type.INKY:
            ghost.x,ghost.y = ghosts_position[2][0], ghosts_position[2][1]
        elif ghost.ghost_type == Ghost_type.CLYDE:
            ghost.x,ghost.y = ghosts_position[3][0], ghosts_position[3][1]
        return (ghost.x, ghost.y)

    def move_ghosts(time) -> None:
        for ghost in self.ghosts:
            
            if ghost.state == Ghost_state.SCATTER:
                target_x, target_x = check_ghost(ghost)
            elif ghosts_state == Ghost_state.CHASE:
                target_x, target_y = self.player.x, self.player.tile_y
            # elif ghost.state == Ghost_state.FRIGHTENED:
            #     target_x,target_y = 

