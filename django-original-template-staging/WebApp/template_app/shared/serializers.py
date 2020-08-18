from rest_framework import serializers
from .models import testData
from .models import trimData
from .models import metaData

class testDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = testData
        fields = '__all__'

class trimDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = trimData
		fields = '__all__'

class metaDataSerializer(serializers.ModelSerializer):

	class Meta:
		model = metaData
		fields = '__all__'
