from django.db import models



class Find(models.Model):
	name = models.CharField(maxlength=100)
	identifier = models.CharField(maxlength=20,unique=True)
	description = models.CharField(maxlength=2000)
	age = models.IntegerField()
	sex = models.IntegerField()
	tagged = models.BooleanField()
	time = models.CharField(maxlength=200)
	latitude = models.FloatField()
	longitude = models.FloatField()
	
	
	class Admin:
		pass

class Image(models.Model):
	filename = models.CharField(maxlength=100,unique=True)
	recordid = models.ForeignKey(Find)
	description = models.CharField(maxlength=100)
	def __str__(self):
		return self.filename

	class Admin:
		pass

class Instance(models.Model):
	name = models.CharField(maxlength=100)
	description = models.CharField(maxlength=2000)
	recordId=models.ForeignKey(Find)
	time = models.CharField(maxlength=20)
	latitude = models.FloatField()
	longitude = models.FloatField()
	observed = models.CharField(maxlength=20)
	
	class Admin:
		pass