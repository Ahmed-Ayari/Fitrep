class RepCounter:
    def __init__(self, down_threshold=140, up_threshold=50):
        self.state = 'DOWN'
        self.count = 0
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold

    def update(self, angle):
        if self.state == 'DOWN' and angle < self.up_threshold:
            self.state = 'UP'

        elif self.state == 'UP' and angle > self.down_threshold:
            self.state = 'DOWN'
            self.count += 1  # rep completes on return to DOWN

    def reset(self):
        self.count = 0
        self.state = 'DOWN'

    def get_count(self):
        return self.count
    
    def get_state(self):
        return self.state