class Location:
    x: float = 0.4202597402597403
    y: float = 0.10962767957878902

    @classmethod
    def get(self) -> [float, float]:
        return self.x, self.y
