from enum import Enum

class Powertrain():
    class Direction(Enum):
        Forward = (-2000, -2000, -2000, -2000)
        Back = (2000, 2000, 2000, 2000)
        Left = (-2000, 2000, -2000, 2000)
        Right = (2000, -2000, 2000, -2000)
        Stop = (0, 0, 0, 0)
        
    def from_str_virtual(direction: str, orientation: str):
        if direction == "forward":
            if orientation == "north":
                return (0, 1)
            elif orientation == "south":
                return (0, -1)
            elif orientation == "east":
                return (1, 0)
            elif orientation == "west":
                return (-1, 0)

            elif direction == "back":
                if orientation == "north":
                    return (0, -1)
                elif orientation == "south":
                    return (0, 1)
                elif orientation == "east":
                    return (-1, 0)
                elif orientation == "west":
                    return (1, 0)

        elif direction == "left":
            gir = ["north", "west", "south", "east"]
            return gir[(gir.index(orientation) + 1) % 4]

        elif direction == "right":
            gir = ["north", "east", "south", "west"]
            return gir[(gir.index(orientation) + 1) % 4]
            
        else:
            log.warn("Stopping car due to unknown direction")
            return (0, 0)
