
import random
from .noise_util import NoiseUtil
import math

# A class of utilities for generating height maps.
# A height is a float in the range of [0.0, 1.0], where
# anything below WATER_THRESHOLD is considered water.

class Terraform:
    WATER_THRESHOLD = 0.53

    @staticmethod
    def simplex(width, height):
        base = random.randint(0, 10000)
        x0 = random.randint(0, 100000)
        y0 = random.randint(0, 100000)

        hyp_x = width / (2 * math.pi)
        hyp_y = height / (2 * math.pi)

        return [[NoiseUtil.make_noise4(
            x0 + (math.cos((x / width) * (2 * math.pi)) * hyp_x), y0 + y,
            x0 + (math.sin((x / width) * (2 * math.pi)) * hyp_x), y0 + y) for x in range(width)]
                for y in range(height)]

    def flat(width, height):
        return [[0.6 for x in range(width)]
            for y in range(height)]
