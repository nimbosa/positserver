from django.db import models

class images(models.Model):
	filename = models.CharField(maxlength=100)
	recordid = models.CharField(maxlength=20)
	
	def __str__(self):
		return self.filename

	class Admin:
		pass

class Finds(models.Model):
	identifier = models.CharField(maxlength=20)
	description = models.CharField(maxlength=2000)
	latitude = models.IntegerField()
	longitude = models.IntegerField()
	type = models.CharField(maxlength=100)

	class Admin:
		pass
