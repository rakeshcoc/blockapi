from rest_framework import generics,mixins,status
from .models import transaction,blocks
from .serializers import transactionSerializer,blocksSerializer,loginSerializer
from django.http import HttpResponse
import json
import block.function
from django.core import serializers
from .models import blocks
import hashlib
from datetime import datetime
from rest_framework.views import APIView
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
class transaction_create(mixins.CreateModelMixin,generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = transactionSerializer
	authentication_classes = (BasicAuthentication,TokenAuthentication ) #OR Type
	permission_classes = (IsAuthenticated,)  #And Type

	def get_queryset(self):
		x = transaction.objects.all()[:5]
		return x

	def post(self,request,*args,**kwargs):
		x =block.function.t_count()
		if(x % 10 == 1):
			data = transaction.objects.all()[x-10:x]
			txn = []
			for i in data:
				dt = i.created_at
				date_time = dt.strftime("%m/%d/%Y, %H:%M:%S")
				set1 = {"txn_id":i.pk,"sender":i.sender,"receiver":i.receiver,"value":i.value,"created_at":date_time,}
				txn.append(set1)
			y = json.dumps(txn)
			current_hash = hash(y)
			z = blocks.objects.last()
			if blocks.objects.last() is None:
				body={"hashprev":0,"txn":txn}
			else:
				body={"hashprev":z.header,"txn":txn}
			b = blocks.objects.create(header=current_hash,body=body)
			b.save()



		return self.create(request,*args,**kwargs)

class transaction_view(generics.RetrieveUpdateAPIView):
	lookup_field = 'pk'
	serializer_class = transactionSerializer
	authentication_classes = (BasicAuthentication,TokenAuthentication )
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		return transaction.objects.all()

class blocks_view(generics.RetrieveAPIView):
	lookup_field='pk'
	serializer_class=blocksSerializer
	authentication_classes = (BasicAuthentication,TokenAuthentication )
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		return blocks.objects.all()

class blocklist(generics.ListAPIView):
	serializer_class=blocksSerializer
	authentication_classes = (BasicAuthentication,TokenAuthentication )
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		x=blocks.objects.all()
		return x

def sample(request,id):
	x =blocks.objects.filter(body__txn__contains=[{'txn_id':id}])
	authentication_classes = (BasicAuthentication,TokenAuthentication )
	permission_classes = (IsAuthenticated,)
	
	return HttpResponse(x)

class loginView(APIView):
	def post(self,request):
		serializer = loginSerializer(data = request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data["user"]
		django_login(request,user)
		data = request.data
		Token.objects.filter(user=user).delete()
		token, created = Token.objects.get_or_create(user=user)
		return Response({"token":token.key},status=200)

class logoutView(APIView):
	auth_class = (TokenAuthentication,)
	authentication_classes = (BasicAuthentication,TokenAuthentication )
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		s=request.headers['Authorization']
		x=s[6:]
		Token.objects.filter(key=x).delete()
		django_logout(request)
		return Response({'msg':"Logout Successful"},status=200)
