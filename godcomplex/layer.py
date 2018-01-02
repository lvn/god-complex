
import itertools

# An abstract object consisting of a collection of "layers", which in aggregate
# represent all the known information about some two-dimensional object (e.g.
# basically any map-like construct).
# Conceptually, a layer is a two-dimensional key-value map in which each value
# represents some attribute about the world in a specific location (or *cell*).
# for easy ser/de purposes (eventually!), layers should be managed through the
# _add_layer, _get_layer_value, _set_layer_value API.
# For convenience, _add_layer also adds the helper getter/setter methods to the
# object itself.

class LayerCollection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = {}

    def _add_layer(self, name, full_layer=None, defaultval=0.0):
        layer = full_layer or [[defaultval for x in range(self.width)]
            for y in range(self.height)]
        setattr(self, name, layer)
        self.layers[name] = layer

        # HACK: adding helper methods to make code cleaner.
        # It's a bit unfortunate that the set of layers will be a bit implicit,
        # but I think it's fine for now.
        setattr(self, 'set_{}'.format(name),
            lambda x, y, val: self._set_layer_value(name, x, y, val))
        setattr(self, 'get_{}'.format(name),
            lambda x, y: self._get_layer_value(name, x, y))
        setattr(self, 'mutate_{}'.format(name),
            lambda x, y, fn: self._mutate_layer_value(name, x, y, fn))

    def _get_layer_value(self, name, x, y):
        try:
            return self.layers[name][y][x]
        except KeyError:
            return None

    def _set_layer_value(self, name, x, y, val):
        self.layers[name][y][x] = val

    def _mutate_layer_value(self, name, x, y, fn):
        fn(self.layers[name][y][x])

    def _all_cells(self):
        return itertools.product(range(self.width), range(self.height))
