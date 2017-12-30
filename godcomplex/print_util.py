
from PIL import Image
import math
import random
from .terraform import Terraform

class PrintUtil:
    @staticmethod
    def get_height_class(h):
        if h <= Terraform.WATER_THRESHOLD:
            return 0
        else:
            return int(math.ceil((h - Terraform.WATER_THRESHOLD) / 0.15))

    @staticmethod
    def render_tile(h):
        height_class = PrintUtil.get_height_class(h)
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
            ''.join([str(world._get_layer_value(layer_name, x, y) or ' ')
                for x in range(world.width)]) for y in range(world.height)]))

    @staticmethod
    def print_terrain(terrain):
        print('\n'.join([
            ''.join([
                PrintUtil.render_tile(h) for h in row
            ]) for row in terrain]))

    @staticmethod
    def print_height_classes(terrain):
        print('\n'.join([
            ''.join([
                str(PrintUtil.get_height_class(h) or ' ') for h in row
            ]) for row in terrain]))
