
import math

class Geometry:
    @staticmethod
    def distance_2d(cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        return math.sqrt((abs(x2 - x1) ** 2) + (abs(y2 - y1) ** 2))
