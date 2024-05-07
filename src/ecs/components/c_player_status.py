from enum import Enum

class PlayerStatus(Enum):
    ALIVE = 0,
    DEAD = 1

class CPlayerStatus:
    def __init__(self, lives) -> None:
        self.status:PlayerStatus = PlayerStatus.ALIVE
        self.lives = lives
        self.dead_time = 4
        self.curr_dead_time = 0