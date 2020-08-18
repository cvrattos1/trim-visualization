# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse


# DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import filters
from rest_framework import serializers
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from django_filters import rest_framework as filters


# application
from WebApp.template_app.shared.models import testData
from WebApp.template_app.shared.serializers import testDataSerializer

from WebApp.template_app.shared.models import trimData
from WebApp.template_app.shared.serializers import trimDataSerializer

from WebApp.template_app.shared.models import metaData
from WebApp.template_app.shared.serializers import metaDataSerializer

import pprint
import os
import json
import sys
import logging
import re

logger = logging.getLogger(__name__)

# Outputs the metadata table as an array of objects
class MetaData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataset = metaData.objects.values()
        return Response(dataset)

# Outputs the entire trim dataset as an array of objects (This can then be parsed by javascript to get correct information
# but ideally more selective django filtering should be used)
class TotalData(APIView):
    def get(self, request, format=None):
        dataset = trimData.objects.values()
        return Response(dataset)

# Outputs data corresponding to Total: Benefits (used by multiyearline.html to graph total eligible and participating benefits
# over multiple years. Example of filtering that could be made easier by using metadata filtering
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataset = trimData.objects.filter(tableid__exact='B1').filter(subtype__exact='4').filter(type__exact='5')
        dataset = dataset.values()
        return Response(dataset)

# Experiment with using metadata queries chained to trim queries
class MetaDataTest(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        columns = metaData.objects.filter(table__exact='B1').filter(short_label__in=['Annual Eligible', 'Annual Particip'])
        dataset = trimData.objects.filter(tableid__in=columns.values("table"))
        dataset = dataset.values()
        return Response(dataset)

# Returns the entirety of the S1 state data table for 2017 (to be further filtered by javascript)
class StateData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataset = trimData.objects.filter(tableid__exact='S1').filter(simulationid__exact='SN2017_')
        dataset = dataset.values()
        return Response(dataset)

# Experiment with returning specific state data using metadata querying (Can only figure out how to 
# filter by rows and tables not columns)
class StateEligibleData(APIView):
    def get(self, request, format=None):
        columns = metaData.objects.filter(table__exact='S1').filter(short_label__exact='Eligible: Annual Benefits')
        dataset = trimData.objects.filter(tableid__in=columns.values("table")).filter(simulationid__exact='SN2017_')
        dataset = dataset.values()
        return Response(dataset)

# API Endpoint with the data for two different S1 tables (State Data)
class MultipleData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataset = trimData.objects.filter(tableid__exact='S1').exclude(type__exact='52').filter(simulationid__in=['SN2017_', 'SN2016_'])
        dataset = dataset.values()
        return Response(dataset)

class LineChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        dataset = trimData.objects.filter(tableid__exact='B1').filter(subtype__exact='4').exclude(type__exact='52')
        dataset = dataset.values()
        return Response(dataset)

class testDataApiView(ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = testDataSerializer
    queryset = testData.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("id", "calendar_year", "variable",)

class trimDataApiView(ReadOnlyModelViewSet):
	serializer_class = trimDataSerializer
	queryset = trimData.objects.all()

	filter_backends = (filters.DjangoFilterBackend,)
	filterset_fields = ("id", "tableid", "type", "subtype")

class metaDataApiView(ReadOnlyModelViewSet):
    serializer_class = metaDataSerializer
    queryset = metaData.objects.all()

