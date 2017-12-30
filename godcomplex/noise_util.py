
from noise import pnoise2, snoise2, snoise4
import random

class NoiseUtil:
    @staticmethod
    def make_noise(x, y, base=0, octs=8, scalex=2, scaley=2):
        freq = 4 * octs
        return (0.5 + (0.1 * random.random()) +
            (0.9 * snoise2(x / (freq * scalex), y / (freq * scaley), octaves=octs, base=base)))

    @staticmethod
    def make_noise4(x, y, z, w, octs=8, scalex=1.5, scaley=1):
        freq = 4 * octs
        return (0.5 + snoise4(
            x / (freq * scalex),
            y / (freq * scaley),
            z / (freq * scalex),
            w / (freq * scaley),
            octaves=octs))
