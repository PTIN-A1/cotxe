class Location:
    x: float = 0.5015634772
    y: float = 0.3986866792

    @classmethod
    def get(self) -> [float, float]:
        return self.x, self.y
