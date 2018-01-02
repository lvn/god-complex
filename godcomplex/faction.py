
import random
import string
from colors import color, COLORS

# hacky: directly represent ansi colors
colors = list(COLORS)
random.shuffle(colors)

class Faction:
    def __init__(self, people, name=None):
        self.people = people
        self.color = colors.pop(0)

        # TODO: better random name generation, obviously
        self.name = 'The First Tribe of {}'.format(string.capwords(people.name))

    def __repr__(self):
        return '<Faction {}>'.format(color(self.name, self.color))
