# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.gis.geos import Point, MultiPoint, Polygon

import logging

logger = logging.getLogger('textlogger')

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class SWRunningInfo(models.Model):
    software_version = models.TextField(primary_key=True, blank=True)
    timestamp_start = models.DateTimeField(null=True, auto_created=False, auto_now=False, blank=True)
    timestamp_stop = models.DateTimeField(null=True, auto_created=False, auto_now=False, blank=True)
    run_id = models.IntegerField(blank=True, null=True)
    counter_observables = models.IntegerField(blank=True, default=0, null=True)
    counter_device_registered = models.IntegerField(blank=True, default=0, null=True)
    counter_message_output = models.IntegerField(blank=True, default=0, null=True)

    class Meta:
        db_table = 'sw_running_info'
