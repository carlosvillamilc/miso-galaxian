class CVerticalCard:
    def __init__(self, speed:float, target_start_y:int, target_end_y:int) -> None:
        self.started = False
        self.speed = speed
        self.target_start_y = target_start_y
        self.target_end_y = target_end_y