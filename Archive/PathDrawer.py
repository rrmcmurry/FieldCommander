import time

class PathDrawer:
    def __init__(self, update_interval=0.5):
        self.path = []
        self.drawing = False
        self.last_update_time = 0
        self.update_interval = update_interval

    def start_drawing(self, start_point):
        self.path = [start_point]
        self.drawing = True
        self.last_update_time = time.time()

    def update_path(self, current_point):
        if self.drawing and time.time() - self.last_update_time > self.update_interval:
            self.path.append(current_point)
            self.last_update_time = time.time()

    def stop_drawing(self):
        self.drawing = False
        completed_path = self.path
        self.path = []
        return completed_path
