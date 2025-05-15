class Location:
    x: float = 0.5015634772
    y: float = 0.3986866792

    @classmethod
    def get(cls) -> [float, float]:
        return cls.x, cls.y
