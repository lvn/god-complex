
import itertools
import random
from .noise_util import NoiseUtil
from .print_util import PrintUtil
from .terraform import Terraform
from .directions import Directions

MAX_NUM_ATTEMPTS = 1000
MAX_NUM_RIVERS = 20

# A World is essentially a collection of "layers". Conceptually, a layer is a
# two-dimensional key-value map in which each value represents some
# attribute about the world in a specific location (or *cell*).
# for easy ser/de purposes (eventually!), layers should be managed through the
# _add_layer, _get_layer_value, _set_layer_value API.

class World:
    def __init__(self, width=250, height=60):
        self.width = width
        self.height = height
        self.layers = set()

    def _add_layer(self, name, full_layer=None, defaultval=0.0):
        layer = full_layer or [[defaultval for x in range(self.width)]
            for y in range(self.height)]
        setattr(self, name, layer)
        self.layers.add(name)

        # HACK: adding helper methods to make code cleaner.
        # It's a bit unfortunate that the set of layers will be a bit implicit,
        # but I think it's fine for now.
        setattr(self, 'set_{}'.format(name),
            lambda x, y, val: self._set_layer_value(name, x, y, val))
        setattr(self, 'get_{}'.format(name),
            lambda x, y: self._get_layer_value(name, x, y))

    def _get_layer_value(self, name, x, y):
        return getattr(self, name)[y][x]

    def _set_layer_value(self, name, x, y, val):
        getattr(self, name)[y][x] = val

    def _all_cells(self):
        return itertools.product(range(self.width), range(self.height))

    def random_cell(self, min_elevation=Terraform.WATER_THRESHOLD):
        h = 0
        num_attempts = 0
        while h < min_elevation:
            if num_attempts >= MAX_NUM_ATTEMPTS:
                raise RuntimeError(
                    'Ran out of tries to get random cell with min_elevation={}'.format(min_elevation))
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            h = self.get_elevation(x, y)
            num_attempts += 1
        return (x, y)

    def get_neighbors(self, x, y):
        adjacent_x = [(x - 1) % self.width, (x + 1) % self.width]
        adjacent_y = [yi for yi in [y - 1, y + 1] if yi >= 0 and yi < self.height]
        return itertools.product(adjacent_x, adjacent_y)

    def get_elevation(self, x, y):
        return self._get_layer_value('terrain', x, y)

    def set_elevation(self, x, y, elevation):
        self._set_layer_value('terrain', x, y, elevation)

    def get_neighbor(self, x, y, direction):
        dx, dy = direction
        xi, yi = (x + dx) % self.width, y + dy

        if yi >= 0 and yi < self.height:
            return (xi, yi)
        return None

    def init_terrain(self):
        print('Generating terrain...')
        self._add_layer('terrain',
            full_layer=Terraform.simplex(self.width, self.height))
        PrintUtil.print_terrain(self.terrain)
        return self

    def init_moisture(self):
        print('Generating moisture...')
        self._add_layer('moisture')
        self.init_rivers()

        # do some kind of bfs to set moisture values
        q = [(cell, 9) for cell in self._all_cells()
            if self.get_moisture(*cell) == 9]
        visited = set()
        while q:
            cell, value = q.pop(0)
            if (cell in visited or
                value <= 0 or
                ):
                continue
            visited.add(cell)
            self.set_moisture(*cell, val=int(value))
            for neighbor in self.get_neighbors(*cell):
                q.append((neighbor, value - 0.5))

        PrintUtil.print_digit_layer(self, 'moisture')
        return self

    # generates rivers using the droplet algorithm.
    def init_rivers(self):
        for i in range(random.randint(MAX_NUM_RIVERS / 2, MAX_NUM_RIVERS)):
            source = self.random_cell()
            curdir = Directions.random()
            curpos = source
            while curpos and self.get_elevation(*curpos) > Terraform.WATER_THRESHOLD:
                # temp hack: set to water by making height 0
                self.set_elevation(*curpos, elevation=0.0)
                self.set_moisture(*curpos, val=9)
                next_cell = self.get_neighbor(*curpos, direction=curdir)
                if not next_cell or self.get_elevation(*next_cell) >= self.get_elevation(*curpos):
                    curdir = Directions.random()
                    next_cell = self.get_neighbor(*curpos, direction=curdir)
                curpos = next_cell
        return self

    def init_resources(self):
        pass

    def place_agent(self):
        pass

    def place_structure(self):
        pass

    def init_peoples(self):
        # return the "Eden agent"
        return self

    def step(self):
        return self
