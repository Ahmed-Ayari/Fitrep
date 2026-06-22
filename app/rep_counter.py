class RepCounter:
    def __init__(self, down_threshold, up_threshold):
        self.state = 'init'
        self.count = 0
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold

    def update(self, angle):
        if self.state == 'init':
            if angle > self.down_threshold:
                self.state = 'DOWN'
        elif self.state == 'DOWN' and angle < self.up_threshold:
            self.state = 'UP'

        elif self.state == 'UP' and angle > self.down_threshold:
            self.state = 'DOWN'
            self.count += 1  # rep completes on return to DOWN

    def reset(self):
        self.count = 0
        self.state = 'init'

    def get_count(self):
        return self.count
    
    def get_state(self):
        return self.state