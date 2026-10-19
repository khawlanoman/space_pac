from .constants import Directions, Ghost_type, Ghost_state

class GhostState:
    def __init__(self,x:float=0.0,y:float=0.0, direction:Directions= Directions.LEFT,
                 ghost_type:Ghost_type= Ghost_type.BLINKY,state:Ghost_state= Ghost_state.SCATTER,
                 my_corner:tuple[int,int]=(0,0),
                 respawn_time:float=30.0,speed:float=4.0, ghost_freaid:float=0.0) -> None:

                 self.x = x 
                 self.y = y 
                 self.direction = direction
                 self.ghost_type = ghost_type
                 self.state = state
                 self.my_corner =my_corner
                 self.respawn_time = respawn_time
                 self.ghost_freaid = ghost_freaid
                 self.speed = speed
    

    def ghosts_dict(self) -> dict:
        ghosts_result = {"x":self.x,
                         "y":self.y,
                         "direction":self.direction.name.lower(),
                         "ghosts_type":self.ghost_type.value,
                         "state":self.state.value,
                         "my_corner":self.my_corner,
                         "respawn_time":self.respawn_time,
                         "speed":self.speed}
        
        return ghosts_result