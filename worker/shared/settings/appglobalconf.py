from shared.settings.base import *
from shared.settings.dockersconf import *
from shared.settings.version import SW_VERSION
from shared.settings.appstableconf import *
from general_types.labelsdictionaries import LocConfLbls
from general_types.general_enums import TypeQueueDetection
from typing import Dict, List, Any
from general_types.labels import LabelThingsName, LabelDatastreamGeneric
from shared.settings.datastreams import DatastreamWristband, DatastreamCamera
from shared.settings.settings import Settings
from utility.geodesy import GeoPosition

# Database Condocker-composeuration
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

GLOBAL_INFO_ENVIRONMENT = "DEV"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

GOST_IOTID_THING_SFN = os.environ.get('GOST_THINGID_SFN', '5')
GOST_IOTID_THING_WRISTBAND = os.environ.get('GOST_THINGID_WRISTBAND', '18')
GOST_IOTID_THING_SFN = int(GOST_IOTID_THING_SFN)
GOST_IOTID_THING_WRISTBAND = int(GOST_IOTID_THING_WRISTBAND)

GOST_DB_THINGS = {
    "value":
        [
            {
             LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: GOST_IOTID_THING_SFN,
             LabelDatastreamGeneric.LABEL_DSGENERIC_NAME: LabelThingsName.LABEL_THING_SFN,
             LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR: "Security Fusion Node",
             LabelDatastreamGeneric.LABEL_DSGENERIC_PROPERTY:
                 {
                    "type": "Video Processing Framework"
                 },
            },
            {
                LabelDatastreamGeneric.LABEL_DSGENERIC_IOTID: GOST_IOTID_THING_WRISTBAND,
                LabelDatastreamGeneric.LABEL_DSGENERIC_NAME: LabelThingsName.LABEL_THING_WRISTBAND,
                LabelDatastreamGeneric.LABEL_DSGENERIC_DESCR: "Wristband Gateway by DEXELS",
                LabelDatastreamGeneric.LABEL_DSGENERIC_PROPERTY: {
                    "type": "Integration Gateway for 868 and UWB Wristbands"
                },
            },
        ]
}

GOST_DATASTREAMS_SFN = {
   "value": [
       DatastreamCamera(iot_id=Settings.CAMERA_IOTID,
                        name=Settings.CAMERA_NAME,
                        gpp=GeoPosition(latitude=Settings.CAMERA_GPP_LATITUDE,
                                        longitude=Settings.CAMERA_GPP_LONGITUDE),
                        ground_plane_size=[Settings.CAMERA_NUMBER_ROWS,
                                           Settings.CAMERA_NUMBER_COLS],
                        gpo=Settings.CAMERA_GPO).to_dict()
    ]
}


GOST_DATASTREAMS_WRISTBAND = {
   "value": DatastreamWristband.get_datastreams_wristbands(iot_id_start=Settings.WRISTBAND_ID_START,
                                                           counter_datastreams=Settings.COUNT_WRISTBANDS)
}


LOCAL_CONFIG_THINGS = {
   LabelThingsName.LABEL_THING_SFN: GOST_DATASTREAMS_SFN,
   LabelThingsName.LABEL_THING_WRISTBAND: GOST_DATASTREAMS_WRISTBAND
}

SCHEDULER_SETTINGS = {
    "TASK_PROVISIONING": 20,
    "TASK_ALIVEAPP": 60
}
