from peripherals.location.location import Location


class VirtualLocation(Location):
    @classmethod
    def change_location(cls, movement, distance):
        if movement == "forward_x":
            cls.x = cls.x + distance
        if movement == "back_x":
            cls.x = cls.x - distance
        if movement == "forward_y":
            cls.y = cls.y + distance
        if movement == "back_y":
            cls.y = cls.y - distance
