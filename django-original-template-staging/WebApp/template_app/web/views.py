# Django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import View

# DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# App
from WebApp.template_app.shared.models import testData
from WebApp.template_app.shared.models import trimData
from WebApp.template_app.shared.serializers import testDataSerializer

# Python
import pprint
import os
import json
import sys
import logging

logger = logging.getLogger(__name__)

class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'template_app/charts.html')

class MapView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'template_app/map.html')

class newDataPage(TemplateView):
    template_name= 'template_app/newmap.html'

    def get_context_data(self, *args, **kwargs):
        context = super(newDataPage, self).get_context_data(*args, **kwargs)

        dataset = trimData.objects.filter(tableid__exact='S1').filter(simulationid__exact='SN2017_')
        some_data = dataset.values()
        myArray = []
        for i in some_data:
            myArray.append(i['col3'])

        dictionary = json.dumps(myArray)
        context['dictionary'] = json.dumps(myArray)

        return context

class testDataPage(TemplateView):
    template_name = 'template_app/test-data.html'

    def get_context_data(self, *args, **kwargs):
        context = super(testDataPage, self).get_context_data(*args, **kwargs)

        # get query data from model
        some_data = trimData.objects.all()

        # get field names from model
        if some_data.exists():
            fields = some_data.first()._meta.local_fields
        else:
            fields = []

        logger.warning("Check field names")
        logger.warning(fields)
        logger.warning("Check Data")
        logger.warning(some_data)

        # add query data and fields to returned data
        context.update({'some_data': some_data})
        context.update({'fields': fields})

        return context



