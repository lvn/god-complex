
from PIL import Image
import math
import random
from colors import color
from .terraform import Terraform
from .biome import Biome

class PrintUtil:
    @staticmethod
    def render_tile(world, x, y):
        moisture = world._get_layer_value('moisture', x, y) or 0
        if moisture > 5:
            return '≈'

        biome = world._get_layer_value('biome', x, y)
        if biome == Biome.TEMPERATE_FOREST or biome == Biome.WOODLAND:
            return random.choice('♠♣♣♠')
        if biome == Biome.GRASSLAND:
            return random.choice(',')
        if biome == Biome.DESERT:
            return random.choice('~≈')

        height_class = Terraform.get_height_class(world.get_elevation(x, y))
        if height_class == 0:
            return '≈'
        elif height_class == 2:
            return random.choice('⌢⌒')
        elif height_class >= 3:
            return random.choice('▲▲^')
        else:
            return '.'

    @staticmethod
    def color_tile(world, x, y):
        biome = world._get_layer_value('biome', x, y)
        if not biome:
            return 15

        moisture = world._get_layer_value('moisture', x, y) or 0
        if moisture > 5:
            return 27

        if biome == Biome.TUNDRA:
            return 87
        if biome == Biome.TAIGA:
            return 109
        if biome == Biome.GRASSLAND:
            return 'green'
        if biome == Biome.WOODLAND:
            return 22
        if biome == Biome.SHRUBLAND:
            return 65
        if biome == Biome.TEMPERATE_FOREST:
            return 22
        if biome == Biome.TEMPERATE_RAINFOREST:
            return 23
        if biome == Biome.RAINFOREST:
            return 23
        if biome == Biome.DESERT:
            return 226
        if biome == Biome.SAVANNAH:
            return 142
        if biome == Biome.OCEAN:
            return 18

    @staticmethod
    def print_digit_layer(world, layer_name):
        print('\n'.join([
            ''.join([str(int(world._get_layer_value(layer_name, x, y)) or ' ')
                for x in range(world.width)]) for y in range(world.height)]))

    @staticmethod
    def print_terrain(world):
        print('\n'.join([
            ''.join([color(PrintUtil.render_tile(world, x, y),
                fg=PrintUtil.color_tile(world, x, y)) for x in range(world.width)])
                    for y in range(world.height)]))

    @staticmethod
    def print_height_classes(terrain):
        print('\n'.join([
            ''.join([
                str(PrintUtil.get_height_class(h) or ' ') for h in row
            ]) for row in terrain]))
