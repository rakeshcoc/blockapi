from rest_framework import serializers
from .models import transaction,blocks
from rest_framework import exceptions
from django.contrib.auth import authenticate
class transactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = transaction
		fields = ['pk','sender','receiver','value','created_at']
		lookup_field = 'pk'

class blocksSerializer(serializers.ModelSerializer):
	class Meta:
		model = blocks
		fields = ['pk','header','body',]
		lookup_field = 'pk'

class loginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self,data):
		username = data.get("username","")
		password = data.get("password","")

		if username and password:
			user = authenticate(username=username,password=password)
			if user:
				data['user'] = user
				
			else:
				raise exceptions.ValidationError("Enter correct username and password")
		else:
			raise exceptions.ValidationError("Enter both username and password")
			
		return data


