class CBlink():
    def __init__(self, rate: float, current_rate: float = 0):
        self.rate: float = rate
        self.current_rate: float = current_rate
        self.enabled = True