from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
from .shared.models import testData
from .shared.models import trimData
from .shared.models import metaData

# Register your resources here.
from .resources import TestDataResource
from .resources import TrimDataResource
from .resources import MetaDataResource

class TestDataAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = TestDataResource
    list_display = ("id", "calendar_year", "variable", "trust_fund_ratio",
                    "cost_payroll", "income_cost", "audit_datetime", )

    search_fields = ['id']
    ordering = ('-id',)

    def get_ordering(self, request):
        return ['id']

class TrimDataAdmin(ImportExportMixin, admin.ModelAdmin):
	resources_class = TrimDataResource
	list_display = ("id", "simulation", "simulationid", "tableid", "type", 
					"subtype", "col1", "col2", "col3", "col4", "col5",
					"col6", "col7", "col8", "col9", "col10")

	search_fields = ['id']
	ordering = ('-id',)

	def get_ordering(self, request):
		return ['id']

class MetaDataAdmin(ImportExportMixin, admin.ModelAdmin):
	resources_class = MetaDataResource
	list_display = ("id", "table", "dimension", "type", "subtype", "short_label", "long_label")
	search_fields = ['id']
	ordering = ('-id',)

	def get_ordering(self, request):
		return ['id']

admin.site.register(testData, TestDataAdmin)
admin.site.register(trimData, TrimDataAdmin)
admin.site.register(metaData, MetaDataAdmin)



