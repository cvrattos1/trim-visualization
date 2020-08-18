from import_export import resources
from .shared.models import testData
from .shared.models import trimData
from .shared.models import metaData

class TestDataResource(resources.ModelResource):
    class Meta:
        model = testData
        import_id_fields = ['id']
        exclude = ('audit_datetime',)

class TrimDataResource(resources.ModelResource):
	class Meta:
		model = trimData
		import_id_fields = ['id']

class MetaDataResource(resources.ModelResource):
	class Meta:
		model = metaData
		import_id_fields = ['id']