
from godcomplex import World
from godcomplex import PrintUtil
import numpy
from PIL import Image

if __name__ == '__main__':
    world = World()

    print('Generating terrain...')
    world.init_terrain()
    PrintUtil.print_terrain(world)
    print('========================')

    print('Generating moisture...')
    world.init_moisture()
    PrintUtil.print_digit_layer(world, 'moisture')
    print('========================')
    PrintUtil.print_terrain(world)
    print('========================')

    print('Generating biomes...')
    world.init_biomes()
    PrintUtil.print_terrain(world)
    print('========================')


    Image.fromarray(numpy.asarray(world.terrain) * 255) \
        .convert('RGB') \
        .save('test.bmp')
