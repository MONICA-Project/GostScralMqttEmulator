from utility.geodesy import GeoPosition
from shared.settings.settings import GeoRefArea
import random


class CalculatePosition:
    @staticmethod
    def calculate_position(ref_pos: GeoPosition, georefarea: GeoRefArea) -> GeoPosition:
        try:
            new_east = random.uniform(a=0, b=georefarea.geoarea_max_east)
            new_north = random.uniform(a=0, b=georefarea.geoarea_max_north)

            return_pos = ref_pos.get_copy()

            return_pos = return_pos.add_enu_distance(enu_distance=[new_east,
                                                                new_north])

            return return_pos
        except Exception as ex:
            print('calculate_position Exception: {}'.format(ex))
