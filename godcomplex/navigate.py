
import heapq
from .biome import Biome

BIOME_COSTS = {
    frozenset([Biome.GRASSLAND, Biome.WOODLAND, Biome.SHRUBLAND]): 1,
    frozenset([Biome.TEMPERATE_FOREST, Biome.TEMPERATE_RAINFOREST,
        Biome.SAVANNAH]): 2,
    frozenset([Biome.SWAMP, Biome.RAINFOREST]): 3,
    frozenset([Biome.DESERT, Biome.TUNDRA]): 4
}

class Path:
    def __init__(self, waypoints, cost):
        self.waypoints = waypoints
        self.cost = cost

    def __repr__(self):
        return '<Path cost={} waypoints={}>'.format(
            self.cost, self.waypoints)

    def __iter__(self):
        return iter(self.waypoints)

class Navigate:
    @staticmethod
    def get_move_cost(world, coord):
        biome = world.get_biome(*coord)
        for biomes, cost in BIOME_COSTS.items():
            if biome in biomes:
                return cost
        return float('inf')

    @staticmethod
    def path(world, src, is_dest, get_neighbors=None,
        get_cost=None):
        '''
        A basic abstract Dijkstra-based pathing implementation that lets callers
            implement their own logic for destination criteria, as well as
            graph traversal logic.
        `world` is the World object.
        `src` is the location to path from.
        `is_dest` is a closure with signature world, tuple<int, int> => bool.
            It provides flexible way to define destination conditions.
        `get_neighbors` is a closure with signature world, tuple<int, int> =>
            [tuple<int, int>]. It defaults to world.get_neighbors
        `get_cost` is an optional closure with signature of
            world, tuple<int, int> => number, which lets callers define custom
            cost functions for movement. It defaults to Navigate.get_move_cost.
        '''

        get_neighbors = (get_neighbors or
            (lambda world, coord: world.get_neighbors(*coord)))
        get_cost = (get_cost or Navigate.get_move_cost)

        q = [(0, tuple([src]))]
        prev_costs = {}
        while q:
            path_cost, path = heapq.heappop(q)
            coord = path[-1]
            if prev_costs.get(coord, float('inf')) <= path_cost:
                continue
            prev_costs[coord] = path_cost
            if is_dest(world, coord):
                return Path(path, path_cost)
            for neighbor in get_neighbors(world, coord):
                move_cost = get_cost(world, neighbor)
                if move_cost < float('inf'):
                    heapq.heappush(q,
                        (path_cost + move_cost, path + tuple([neighbor])))
        return None
