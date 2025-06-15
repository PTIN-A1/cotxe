class Distance:
    self.obstacle_detected: int = 0
    
    # Si es vol que cada instància tingui el seu self.obstacle_detected:
    # def __init__(self):
    #    self.obstacle_detected: int = 0
    
    @classmethod
    def get(self) -> int:
        return self.obstacle_detected
        
    @classmethod
    def set(self, new_value):
        self.obstacle_detected = new_value
