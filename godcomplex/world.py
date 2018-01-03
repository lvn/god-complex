
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
from .agent import AgentType, AgentActions, Agent
from .people import People
from .faction import Faction
from .history import History

MAX_NUM_ATTEMPTS = 1000
MOISTURE_FACTOR = 0.95
MOISTURE_CLASS = 0.16

class World(LayerCollection):
    def __init__(self, width=300, height=60, db=None):
        super().__init__(width, height)
        self.db = db
        self.agents = {}
        self.factions = {}
        self.pending_agents = []  # pending queue, emptied at the end of every step
        self.history = History()

    def get_agent(self, agent_id):
        return self.agents[agent_id]

    def add_agent(self, agent):
        self.agents[agent.id] = agent

    def add_faction(self, faction):
        self.factions[faction.name] = faction

    def add_pending_agent(self, agent):
        self.pending_agents.append(agent)

    def get_db(self):
        return self.db

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
        max_num_rivers = (self.width * self.height) // 700

        for i in range(max_num_rivers):
            source = self.random_cell(min_elevation=0.8)
            curpos = source
            curdir = Directions.random()
            curelev = self.get_elevation(*source)
            while curpos and self.get_elevation(*curpos) > Terraform.WATER_THRESHOLD:
                self.set_moisture(*curpos, val=1.0)

                next_cell = self.get_neighbor(*curpos, direction=curdir)
                if not next_cell or self.get_elevation(*next_cell) > self.get_elevation(*curpos):
                    directions = [d for d in Directions.all()
                        if self.get_neighbor(*curpos, direction=d) and not self.get_moisture(*self.get_neighbor(*curpos, direction=d))]
                    if not directions:
                        break
                    curdir = random.choice(directions)
                    next_cell = self.get_neighbor(*curpos, direction=curdir)

                curpos = next_cell
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

    def move_agent(self, agent, x, y):
        if agent.position:
            self.mutate_agent_position(*agent.position,
                fn=lambda value: value.remove(agent.id))

        self.mutate_agent_position(x, y, fn=lambda value: value.add(agent.id))
        agent.position = (x, y)

    def place_agent(self, agent):
        agent_position = self.random_cell(min_elevation=0.6)
        self.move_agent(agent, *agent_position)

    def place_structure(self):
        pass

    def init_peoples(self):
        # The agent_positions layer consists of a set of uuids representing
        # the agents on a cell.
        self._add_layer('agent_position',
            full_layer=[[set() for x in range(self.width)]
                for y in range(self.height)])
        self._add_layer('settlement', defaultval=None)

        # return the "Eden agent" (i.e. first settler) for each different
        # people.
        for people in People.all_peoples(self.db, self):
            faction = Faction(people=people)
            self.add_faction(faction)
            agent = Agent(world=self,
                faction=faction,
                agent_type=AgentType.SETTLER,
                goals=[AgentActions.settle])
            self.add_agent(agent)
            self.place_agent(agent)

        return self

    def init_all(self):
        self.init_terrain()
        self.init_moisture()
        self.init_biomes()
        self.init_peoples()

    def step(self):
        for _, agent in self.agents.items():
            self.history.record(agent, *agent.step())

        for agent in self.pending_agents:
            self.add_agent(agent)
            self.history.record(agent, AgentActions.spawn)

        self.history.advance()
