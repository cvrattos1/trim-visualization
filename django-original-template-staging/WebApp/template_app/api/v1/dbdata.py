from WebApp.template_app.shared.models import trimData
from WebApp.template_app.shared.serializers import trimDataSerializer

from WebApp.template_app.shared.models import metaData
from WebApp.template_app.shared.serializers import metaDataSerializer

class database_data():

	def getStateData(self):
		stateData = []
		dataset = trimData.objects.filter(tableid__exact='S1').filter(simulationid__exact='SN2017_')
        
        for i, state in enumerate(dataset):
        	stateData[i] = state.col1

        return stateData