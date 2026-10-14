from .constants import Directions
class PlayerState:
    def __init__(self,x:float=0.0,y:float=0.0,direction:Directions= None, 
                 next_direction:Directions= None,lives:int=3,score:int=0,is_power:bool=False,
                 power_time:float=0.0, speed:float=5.0) -> None:
        self.x = x 
        self.y = y 
        self.direction = direction
        self.next_direction = next_direction
        self.lives = lives
        self.score = score
        self.is_power = is_power
        self.power_time = power_time
        self.speed =speed

    
    def player_dict(self) -> dict:
        player_result ={"x":self.x,
                        "y":self.y,
                        "direction":self.direction.name.lower(),
                        "next_direction": self.next_direction,
                        "lives": self.lives,
                        "is_power":self.is_power,
                        "power_time":self.power_time}

        return player_result

