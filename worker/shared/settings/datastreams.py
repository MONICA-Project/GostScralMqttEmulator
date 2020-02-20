from typing import Dict, Any, List
from utility.geodesy import GeoPosition
from datetime import datetime
from general_types.labels import LabelThingsName, LabelDatastreamGeneric

import logging

logger = logging.getLogger('textlogger')


class Datastream(object):
    def get_altfunc_param(self,
                  label: str,
                  list_labels: List[Dict[str, Any]]) -> Any:
        try:
            if not list_labels:
                return self.get_param(label=label)

            dict_return = dict()
            for dictionary in list_labels:
                if not dictionary:
                    continue

                for sub_label in dictionary.keys():
                    if not sub_label:
                        continue

                    list_labels = dictionary[sub_label]

                    dict_return[sub_label] = self.get_altfunc_param(sub_label,
                                                                    list_labels)
            return dict_return
        except Exception as ex:
            logger.error('get_altfunc_param Exception: {}'.format(ex))
            return None

    def to_dict(self) -> Dict[str, Any]:
        list_labels = self.get_labels()

        if not list_labels:
            return None

        dict_return = dict()

        for dict_label in list_labels:
            if not dict_label:
                continue

            for label in dict_label.keys():
                if not label:
                    continue

                sub_labels = dict_label[label]
                dict_return[label] = self.get_altfunc_param(label=label,
                                                            list_labels=sub_labels)

        return dict_return

    def get_param(self, label: str) -> Any:
        pass

    def get_labels(self) -> List[Dict[str, List[str]]]:
        pass


class LabelDatastramCamera:
    LABEL_DSCAM_GPP = "ground_plane_position"
    LABEL_DSCAM_GPO = "ground_plane_orientation"
    LABEL_DSCAM_GPS = "ground_plane_size"

    @staticmethod
    def get_complete_list() -> List[Dict[str, List[str]]]:
        return [
                {LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: []},
                {LabelDatastreamGeneric.LABEL_DSGENERIC_NAME: []},
                {LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR: []},
                {LabelDatastreamGeneric.LABEL_DSGENERIC_UNITOFMEAS:
                    [
                    {LabelDatastramCamera.LABEL_DSCAM_GPP: []},
                    {LabelDatastramCamera.LABEL_DSCAM_GPO: []},
                    {LabelDatastramCamera.LABEL_DSCAM_GPS: []}
                    ]
                }
        ]


class DatastreamCamera(Datastream):
    def __init__(self,
                 iot_id: int,
                 name: str,
                 gpp: GeoPosition,
                 gpo: int,
                 ground_plane_size: List[int],
                 zone_id: str = "FAKE CAMERA"):
        self.iot_id = iot_id
        self.name = "{0}/Camera/CDL-Estimation/{1}".format(LabelThingsName.LABEL_THING_SFN,
                                                           name)
        self.gpp = gpp
        self.gpo = gpo
        self.ground_plane_size = ground_plane_size
        self.desc = "Datastream for Estimation of Gate-Counting events"
        self.zone_id = zone_id

    def get_labels(self) -> List[Dict[str, List[str]]]:
        return LabelDatastramCamera.get_complete_list()

    def get_param(self, label: str) -> Any:
        if label == LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID:
            return self.iot_id
        elif label == LabelDatastreamGeneric.LABEL_DSGENERIC_NAME:
            return self.name
        elif label == LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR:
            return self.desc
        elif label == LabelDatastramCamera.LABEL_DSCAM_GPP:
            return [
                self.gpp.latitude,
                self.gpp.longitude
                    ]
        elif label == LabelDatastramCamera.LABEL_DSCAM_GPO:
            return self.gpo

        elif label == LabelDatastramCamera.LABEL_DSCAM_GPS:
            return self.ground_plane_size

        return str()


class LabelDatastreamWristband:
    LABEL_DSWRIST_METADATA = "metadata"
    LABEL_DSWRIST_BUTTONID = "buttonId"
    LABEL_DSWRIST_TIMESTAMP = "timestamp"
    LABEL_DSWRIST_TAGID = "tagId"
    LABEL_DSWRIST_TYPE = "type"

    @staticmethod
    def get_complete_list() -> List[Dict[str, List[str]]]:
        return [
                {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: []
                },
                {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_NAME: []
                },
                {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR: []
                },
                {
                    LabelDatastreamGeneric.LABEL_DSGENERIC_UNITOFMEAS:
                    [
                        {LabelDatastreamWristband.LABEL_DSWRIST_METADATA:
                            [
                                {LabelDatastreamWristband.LABEL_DSWRIST_BUTTONID: []},
                                {LabelDatastreamWristband.LABEL_DSWRIST_TIMESTAMP: []},
                                {LabelDatastreamWristband.LABEL_DSWRIST_TAGID: []},
                                {LabelDatastreamWristband.LABEL_DSWRIST_TYPE: []},
                            ]},
                    ]
                }
        ]


class DatastreamWristband(Datastream):
    def __init__(self,
                 iot_id: int,
                 name_id: int):
        self.iot_id = iot_id
        self.timestamp = datetime.utcnow()
        self.name = "WRISTBAND-GW/868/Localization-Wristband/{}".format(name_id)
        self.desc = "Datastream for Estimation of Gate-Counting events"

    def get_labels(self) -> List[Dict[str, List[str]]]:
        return LabelDatastreamWristband.get_complete_list()

    def get_param(self, label: str) -> Any:
        if label == LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID:
            return self.iot_id
        elif label == LabelDatastreamGeneric.LABEL_DSGENERIC_NAME:
            return self.name
        elif label == LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR:
            return self.desc
        elif label == LabelDatastreamWristband.LABEL_DSWRIST_BUTTONID:
            return 1
        elif label == LabelDatastreamWristband.LABEL_DSWRIST_TIMESTAMP:
            return self.timestamp.isoformat()
        elif label == LabelDatastreamWristband.LABEL_DSWRIST_TAGID:
            return str(self.iot_id)
        elif label == LabelDatastreamWristband.LABEL_DSWRIST_TYPE:
            return "868"

        return str()

    @staticmethod
    def get_datastreams_wristbands(iot_id_start: int,
                                   counter_datastreams: int) -> List[Dict[str, Any]]:
        list_ds = list()

        for index in range(0, counter_datastreams):
            list_ds.append(DatastreamWristband(iot_id=iot_id_start+index,
                                               name_id=index+1).to_dict())
        return list_ds
