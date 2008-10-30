from django.db import models



class Find(models.Model):
	name = models.CharField(max_length=100)
	identifier = models.CharField(max_length=20,unique=True)
	description = models.CharField(max_length=2000)
	age = models.IntegerField()
	sex = models.IntegerField()
	tagged = models.BooleanField()
	time = models.CharField(max_length=200)
	latitude = models.FloatField()
	longitude = models.FloatField()
	
	
	class Admin:
		pass

class Image(models.Model):
	filename = models.CharField(max_length=100,unique=True)
	recordid = models.ForeignKey(Find)
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.filename

	class Admin:
		pass

class Instance(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=2000)
	recordId=models.ForeignKey(Find)
	time = models.CharField(max_length=20)
	latitude = models.FloatField()
	longitude = models.FloatField()
	observed = models.CharField(max_length=20)
	
	class Admin:
		pass
	

		