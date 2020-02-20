from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from shared.settings.appglobalconf import GOST_DB_THINGS, GOST_DATASTREAMS_SFN, GOST_DATASTREAMS_WRISTBAND
from api.wp6catalog import WP6Catalog
import logging

logger = logging.getLogger('textlogger')


class GostDBThings(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(GOST_DB_THINGS,
                            safe=False,
                            status=status.HTTP_200_OK)


class GostDBSFNDatastreams(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(GOST_DATASTREAMS_SFN,
                            safe=False,
                            status=status.HTTP_200_OK)


class GOSTWP6CreateNewDatastream(APIView):
    def post(self, request, *args, **kwargs):
        logger.info('GOSTWP6CreateNewDatastream request.data {}'.format(request.data))
        response = WP6Catalog.create_thing(dict_input=request.data)
        return JsonResponse(response,
                            safe=False,
                            status=status.HTTP_200_OK)


class GostDBWristbandDatastreams(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(GOST_DATASTREAMS_WRISTBAND,
                            safe=False,
                            status=status.HTTP_200_OK)
