from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class testData(models.Model):
    id = models.BigIntegerField(db_column='ID', primary_key=True)
    calendar_year = models.IntegerField(
        blank=True, null=True, verbose_name="Calendar Year")
    variable = models.CharField(max_length=150)
    trust_fund_ratio = models.FloatField(blank=True, null=True)
    cost_payroll = models.FloatField(blank=True, null=True)
    income_cost = models.FloatField(blank=True, null=True)
    audit_datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return 'id: {}'.format(self.id)

    class Meta:
        db_table = "test_data"
        managed = False

class trimData(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    simulation = models.CharField(max_length=150)
    simulationid = models.CharField(max_length=150)
    tableid = models.CharField(max_length=150)
    type = models.IntegerField(blank=True, null=True, verbose_name="type")
    subtype = models.IntegerField(blank=True, null=True, verbose_name="subtype")
    col1 = models.FloatField(blank=True, null=True)
    col2 = models.FloatField(blank=True, null=True)
    col3 = models.FloatField(blank=True, null=True)
    col4 = models.FloatField(blank=True, null=True)
    col5 = models.FloatField(blank=True, null=True)
    col6 = models.FloatField(blank=True, null=True)
    col7 = models.FloatField(blank=True, null=True)
    col8 = models.FloatField(blank=True, null=True)
    col9 = models.FloatField(blank=True, null=True)
    col10 = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return 'id: {}'.format(self.id)

    class Meta:
        db_table = "trim_data"
        managed = False

class metaData(models.Model):
    id = models.BigIntegerField(db_column='id', primary_key=True)
    table = models.CharField(max_length=150)
    dimension = models.CharField(max_length=150)
    type = models.IntegerField(blank=True, null=True, verbose_name="type")
    subtype = models.IntegerField(blank=True, null=True, verbose_name="subtype")
    short_label = models.CharField(max_length=150)
    long_label = models.CharField(max_length=250)

    def __unicode__(self):
        return 'id: {}'.format(self.id)

    class Meta:
        db_table = "meta_data"
        managed = False

