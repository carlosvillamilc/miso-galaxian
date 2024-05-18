from enum import Enum

class CTagEnemy:
    def __init__(self, score_value:float, index:int) -> None:
        self.score_value = score_value
        self.index = index
        self.state:EnemyState = EnemyState.MOVING

class EnemyState(Enum):
    MOVING = 0
    STEERING = 1
    RETURNING = 2