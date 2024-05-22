from enum import Enum

class CTagEnemy:
    def __init__(self, score_value:float, index:int, type:str) -> None:
        self.score_value = score_value
        self.index = index
        self.state:EnemyState = EnemyState.MOVING
        self.type = type

class EnemyState(Enum):
    MOVING = 0
    STEERING = 1
    RETURNING = 2