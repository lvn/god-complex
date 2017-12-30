
import random

class Directions:
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)

    @staticmethod
    def all():
        return [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]

    @staticmethod
    def random():
        return random.choice(Directions.all())
