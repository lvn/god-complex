
from PIL import Image
import math
import random
from .terraform import Terraform

class PrintUtil:
    @staticmethod
    def render_tile(world, x, y):
        try:
            if world.get_moisture(x, y) > 5:
                return '≈'
        except AttributeError:
            pass

        height_class = Terraform.get_height_class(world.get_elevation(x, y))
        if height_class == 0:
            return ' '
        elif height_class == 2:
            return random.choice(['⌢', '⌒'])
        elif height_class >= 3:
            return random.choice('▲▲^')
        else:
            return ','

    @staticmethod
    def print_digit_layer(world, layer_name):
        print('\n'.join([
            ''.join([str(int(world._get_layer_value(layer_name, x, y)) or ' ')
                for x in range(world.width)]) for y in range(world.height)]))

    @staticmethod
    def print_terrain(world):
        print('\n'.join([
            ''.join([PrintUtil.render_tile(world, x, y)
                for x in range(world.width)]) for y in range(world.height)]))

    @staticmethod
    def print_height_classes(terrain):
        print('\n'.join([
            ''.join([
                str(PrintUtil.get_height_class(h) or ' ') for h in row
            ]) for row in terrain]))
