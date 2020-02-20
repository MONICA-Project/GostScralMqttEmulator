import datetime
from typing import Dict, List, Any
from django.contrib.gis.geos import Point
from general_types.labels import LabelDatastreamGeneric
from general_types.enumerations import ObservableGenericType
import logging

logger = logging.getLogger('textlogger')


class ObservableGeneric(object):

    def __init__(self, device_id: str, iot_id: int):
        self.iot_id = iot_id
        self.timestamp = datetime.datetime.utcnow()
        self.device_id = device_id

    def to_dictionary(self) -> Dict[str, Any]:
        raise NotImplemented

    def get_device_id(self) -> str:
        return self.device_id

    def get_iot_id(self) -> int:
        return self.iot_id

    def get_timestamp(self) -> datetime.datetime:
        return self.timestamp

    def get_observable_type(self) -> ObservableGenericType:
        raise NotImplemented


class Localization(ObservableGeneric):
    def __init__(self, tag_id: str, iot_id: int, lat: float, lon: float):
        super().__init__(device_id=tag_id, iot_id=iot_id)
        self.type = 868
        self.areaId = "LST"
        self.motion_state = "unknown"
        self.lat = lat # 55.67298336627162
        self.lon = lon # 12.56703788516.0
        self.z = 0.0
        self.bearing = 0.0
        self.height = 0.0
        self.herr = 0.0
        self.battery_level = 2.9

    def to_dictionary(self) -> Dict[str, Any]:
        return {
            LabelDatastreamGeneric.LABEL_DSGENERIC_DATASTREAM: {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: self.get_iot_id()
                },
                LabelDatastreamGeneric.LABEL_DSGENERIC_PHENOMENONTIME: self.timestamp,
                LabelDatastreamGeneric.LABEL_DSGENERIC_RESULT: {
                    "tagId": self.get_device_id(),
                    "type": "868",
                    "areaId": "LST",
                    "motion_state": "unknown",
                    "lat": self.lat,
                    "lon": self.lon,
                    "z": self.z,
                    "bearing": 0.0,
                    "height": 0.0,
                    "herr": 0.0,
                    "battery_level": 2.9,
                    "timestamp": self.get_timestamp().isoformat()
                    }
                }

    def get_observable_type(self) -> ObservableGenericType:
        return ObservableGenericType.LOCALIZATION


class CrowdDensityLocalObservation(ObservableGeneric):
    def __init__(self,
                 device_id: str,
                 iot_id: int,
                 map_size: List[int]):
        super().__init__(device_id=device_id, iot_id=iot_id)
        self.module_id = "435ae19f-0eab-5561-b11a-9ead485180d6_crowd_density_local"

        self.density_map = list()

        if not map_size or len(map_size) < 2:
            return

        for index_row in range(0, map_size[0]):
            list_row = list()
            for index_col in range(0, map_size[1]):
                list_row.append(0)
            self.density_map.append(list_row)

        self.original_densitymap = self.density_map

        # self.original_densitymap = [[0, 0, 1, 2, 1, 1, 1, 0, 0],
        #                             [0, 0, 1, 2, 1, 0, 0, 0, 0],
        #                             [1, 1, 1, 1, 0, 0, 0, 0, 0],
        #                             [0, 2, 0, 0, 0, 0, 0, 0, 0],
        #                             [0, 0, 1, 1, 0, 0, 2, 2, 1],
        #                             [0, 0, 1, 1, 1, 1, 2, 5, 4],
        #                             [0, 0, 0, 0, 1, 2, 1, 3, 3],
        #                             [0, 0, 0, 2, 3, 2, 1, 1, 1],
        #                             [0, 0, 1, 4, 5, 2, 2, 2, 0],
        #                             [0, 0, 1, 4, 3, 1, 5, 5, 1],
        #                             [0, 2, 2, 3, 4, 3, 6, 11, 8],
        #                             [0, 1, 2, 2, 3, 3, 3, 7, 7]]
        #
        # self.density_map = \
        #     [[0, 0, 1, 2, 1, 1, 1, 0, 0],
        #      [0, 0, 1, 2, 1, 0, 0, 0, 0],
        #      [1, 1, 1, 1, 0, 0, 0, 0, 0],
        #      [0, 2, 0, 0, 0, 0, 0, 0, 0],
        #      [0, 0, 1, 1, 0, 0, 2, 2, 1],
        #      [0, 0, 1, 1, 1, 1, 2, 5, 4],
        #      [0, 0, 0, 0, 1, 2, 1, 3, 3],
        #      [0, 0, 0, 2, 3, 2, 1, 1, 1],
        #      [0, 0, 1, 4, 5, 2, 2, 2, 0],
        #      [0, 0, 1, 4, 3, 1, 5, 5, 1],
        #      [0, 2, 2, 3, 4, 3, 6, 11, 8],
        #      [0, 1, 2, 2, 3, 3, 3, 7, 7]]

        self.ground_plane_position = Point(x=0,
                                           y=0,
                                           srid=4326)
        self.density_count = 0
        self.size_area_x = 0
        self.size_area_y = 0

    def reset_density_map(self):
        if len(self.density_map) != len(self.original_densitymap):
            return
        if len(self.density_map[0]) != len(self.original_densitymap[0]):
            return
        self.density_count = 0
        counter_rows = len(self.density_map)
        counter_columns = len(self.density_map[0])

        for index_row in range(0, counter_rows):
            for index_col in range(0, counter_columns):
                self.density_map[index_row][index_col] = self.original_densitymap[index_row][index_col]

    def consolidate_observable(self):
        self.density_count = 0

        counter_rows = len(self.density_map)
        counter_columns = len(self.density_map[0])

        for index_row in range(0, counter_rows):
            for index_col in range(0, counter_columns):
                self.density_count += int(self.density_map[index_row][index_col])

    def set_density_map(self, counter_people: int):
        try:
            self.reset_density_map()

            self.density_count = counter_people
            counter_rows = len(self.density_map)
            counter_columns = len(self.density_map[0])

            current_counter = 0

            while current_counter < self.density_count:
                for index_row in range(0, counter_rows):
                    for index_col in range(0, counter_columns):
                        self.density_map[index_row][index_col] += 1
                        current_counter += 1
        except Exception as ex:
            logger.error('Observable set_density_map Exception: {}'.format(ex))

    def to_dictionary(self) -> Dict[str, Any]:
        try:
            return {
                LabelDatastreamGeneric.LABEL_DSGENERIC_DATASTREAM: {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: self.get_iot_id()
                },
                LabelDatastreamGeneric.LABEL_DSGENERIC_PHENOMENONTIME: self.get_timestamp().isoformat(),
                LabelDatastreamGeneric.LABEL_DSGENERIC_RESULT: {
                        "module_id": self.module_id,
                        "camera_ids": [
                            self.get_device_id()
                        ],
                        "density_map": self.density_map,
                        "timestamp_2": self.get_timestamp().isoformat(),
                        "type_module": "crowd_density_local",
                        "density_count": self.density_count,
                        "timestamp": self.get_timestamp().isoformat()
                    }
                }
        except Exception as ex:
            logger.error('Observable to_dictionary Exception: {}'.format(ex))
            return None

    def get_observable_type(self) -> ObservableGenericType:
        return ObservableGenericType.CROWDDENSITYLOCAL
