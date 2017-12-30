
import math
from .terraform import Terraform

class Biome:
    TUNDRA = 1
    TAIGA = 2
    GRASSLAND = 10
    WOODLAND = 11
    SHRUBLAND = 12
    TEMPERATE_FOREST = 20
    TEMPERATE_RAINFOREST = 21
    RAINFOREST = 22
    DESERT = 30
    SAVANNAH = 31
    OCEAN = 1000

    # celsius, because I am canadian.
    # formula stolen from: http://davidwaltham.com/global-warming-model/
    # TODO: actually account for elevation
    @staticmethod
    def _estimate_avg_temperature(latitude, elevation):
        latitude_temp = 30 - (40 * (math.sin(math.radians(latitude)) ** 2))
        elevation_temp = (elevation - Terraform.WATER_THRESHOLD) * -80

        return latitude_temp + elevation_temp

    # a poor man's Whittaker diagram.
    # latitude and elevation are used as a proxy for average temperature.
    # consider supporting unearthlike axial tilts.
    @staticmethod
    def determine_biome(latitude, elevation, moisture):
        if elevation < Terraform.WATER_THRESHOLD:
            return Biome.OCEAN

        temp = Biome._estimate_avg_temperature(latitude, elevation)
        # ugh.
        if temp <= -5:
            return Biome.TUNDRA
        elif temp <= 3:
            if moisture <= 1:
                return Biome.GRASSLAND
            else:
                return Biome.TAIGA
        elif temp < 20:
            if moisture <= 1:
                if temp < 15:
                    return Biome.GRASSLAND
                else:
                    return Biome.DESERT
            elif moisture <= 2:
                return Biome.WOODLAND
            elif moisture <= 5:
                return Biome.TEMPERATE_FOREST
            else:
                return Biome.TEMPERATE_RAINFOREST
        else:
            if moisture <= 1:
                return Biome.DESERT
            elif moisture <= 4:
                return Biome.SAVANNAH
            else:
                return Biome.RAINFOREST
