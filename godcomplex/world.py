
import itertools
import random
import math
from .noise_util import NoiseUtil
from .print_util import PrintUtil
from .terraform import Terraform
from .directions import Directions
from .biome import Biome
from .geometry import Geometry
from .layer import LayerCollection

MAX_NUM_ATTEMPTS = 1000
MAX_NUM_RIVERS = 30
MOISTURE_FACTOR = 0.95
MOISTURE_CLASS = 0.16

class World(LayerCollection):
    def __init__(self, width=250, height=60):
        super().__init__(width, height)

    def get_latitude(self, x=0, y=0):
        return 90 * (abs(y - (self.height / 2)) / (self.height / 2))

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

    def get_neighbors(self, x, y, diagonals=False):
        adjacent_x = [(x - 1) % self.width, x, (x + 1) % self.width]
        adjacent_y = [yi for yi in [y - 1, y, y + 1]
            if yi >= 0 and yi < self.height]
        return [coord for coord in itertools.product(adjacent_x, adjacent_y)
            if coord != (x, y) and
            (diagonals or (coord[0] == x or coord[1] == y))]

    def get_neighbor(self, x, y, direction):
        dx, dy = direction
        xi, yi = (x + dx) % self.width, y + dy

        if yi >= 0 and yi < self.height:
            return (xi, yi)
        return None

    def init_terrain(self):
        self._add_layer('elevation',
            full_layer=Terraform.simplex(self.width, self.height))
        return self

    def init_moisture(self):
        self._add_layer('moisture')
        self.init_rivers()

        # assign moisture values based on distance from moisture (i.e. river
        # cells). the moisture value exponentially decays as distance increases.
        # cells are traversed using BFS from river tiles to ensure that we visit
        # higher-moisture tiles first.
        q = [(cell, cell) for cell in self._all_cells()
            if self.get_moisture(*cell)]
        visited = set()
        while q:
            cell, src = q.pop(0)
            if (cell in visited or
                not Terraform.get_height_class(self.get_elevation(*cell))):
                continue
            visited.add(cell)
            dist = Geometry.distance_2d(cell, src)
            self.set_moisture(*cell, val=max(1, int((MOISTURE_FACTOR ** dist) / MOISTURE_CLASS)))
            for neighbor in self.get_neighbors(*cell):
                q.append((neighbor, src))
        return self

    # generates rivers using the droplet algorithm.
    def init_rivers(self):
        for i in range(random.randint(MAX_NUM_RIVERS / 2, MAX_NUM_RIVERS)):
            source = self.random_cell(min_elevation=0.75)
            curpos = source
            prev = None
            while curpos and self.get_elevation(*curpos) > Terraform.WATER_THRESHOLD:
                self.set_moisture(*curpos, val=1.0)
                neighbors = [neighbor for neighbor
                    in self.get_neighbors(*curpos)
                    if (self.get_elevation(*neighbor) < self.get_elevation(*curpos)
                        and not self.get_moisture(*neighbor))]

                if not neighbors and prev:
                    curpos = prev
                    prev = None
                elif neighbors:
                    curpos = random.choice(neighbors)
                    prev = curpos
                else:
                    break
        return self

    def init_biomes(self):
        self._add_layer('biome',
            full_layer=[[Biome.determine_biome(
                latitude=self.get_latitude(y=y),
                elevation=self.get_elevation(x, y),
                moisture=self.get_moisture(x, y)
            ) for x in range(self.width)] for y in range(self.height)])
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
