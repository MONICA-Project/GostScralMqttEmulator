"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
import os

from rest_framework import routers

from api.views import GostDBThings, GostDBSFNDatastreams, GostDBWristbandDatastreams, GOSTWP6CreateNewDatastream
from shared.settings.create_urls import create_paths_datastreams
import logging

router = routers.DefaultRouter()
# register job endpoint in the router
# router.register(r'jobs', jviews.JobViewSet)

logger = logging.getLogger('textlogger')

GOST_IOTID_THING_SFN = os.environ.get('GOST_THINGID_SFN', '5')
GOST_IOTID_THING_WRISTBAND = os.environ.get('GOST_THINGID_WRISTBAND', '18')

urlpatterns = [
    path('', include(router.urls)),
    path('admin', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    path('v1.0/Things', GostDBThings.as_view()),  # , name="Emulated GOST Things"
    path('v1.0/Things/', GostDBThings.as_view()),
    path('v1.0/Things({0})/Datastreams'.format(GOST_IOTID_THING_SFN), GostDBSFNDatastreams.as_view()),  # , name="Emulated GOST Things"
    path('v1.0/Things({0})/Datastreams'.format(GOST_IOTID_THING_WRISTBAND), GostDBWristbandDatastreams.as_view()),  # , name="Emulated GOST Things"
    path('SearchOrCreateOGCDataStreamId', GOSTWP6CreateNewDatastream.as_view())
]

# logger.info('Executing List New Path')
#
# list_new_paths = create_paths_datastreams()
#
# if list_new_paths:
#     urlpatterns.extend(list_new_paths)
#     logger.info('Append List New Paths, New List Size: {}'.format(len(urlpatterns)))
# else:
#     logger.info('NOTHING TO APPEND')