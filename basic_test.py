
from godcomplex import World
import numpy
from PIL import Image

if __name__ == '__main__':
    world = World()
    world.init_terrain()
    world.init_moisture()
    Image.fromarray(numpy.asarray(world.terrain) * 255) \
        .convert('RGB') \
        .save('test.bmp')
