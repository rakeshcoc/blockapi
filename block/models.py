from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class  transaction(models.Model):
	sender = models.CharField(max_length = 200)
	receiver = models.CharField(max_length = 200)
	value = models.IntegerField()
	created_at =models.DateTimeField(auto_now_add = True,blank=True)
	def __str__(self):
		return str(self.pk)

class blocks(models.Model):
	header =models.CharField(max_length=100,default="null")
	body = JSONField()
	def __str__(self):
		return str(self.pk)
