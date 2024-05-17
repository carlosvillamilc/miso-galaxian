class GlobalsService:
    def __init__(self) -> None:
        self.player_lives = 3
        self.player_score = 0
        self.player_previous_score = 0
        self.player_high_score = 0
        self.current_level = 1
        self.next_level_cooldown = 5
        self.paused = False

    def game_over(self):
        self.player_lives = 3
        self.player_previous_score = 0
        self.player_score = 0
        self.current_level = 1
        self.next_level_cooldown = 5

    def next_level(self):
        self.current_level += 1
        self.next_level_cooldown = 5
