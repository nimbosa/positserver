from django.shortcuts import render_to_response
import sqlite3 as sqldb
from models import images as Images
from models import Finds
from django.db.models import Q

def home(request):
	appdata = "POSIT"
	return render_to_response("home.html",{"appdata":appdata})


def images(request):
	all_images = Images.objects.all()
	return render_to_response("images.html",{"images":all_images})


def stats(request):
	all_finds= Finds.objects.all()
	return render_to_response("stats.html",{"finds":all_finds})

def map(request):
	all_finds= Finds.objects.all()
	print all_finds
	imageList = []
	ids = []
	for find in all_finds:
		images=Images.objects.filter(recordid=find.identifier)
		#imageDict[find.identifier] = images.
		#images = Images.objects.all()
		ids.append(find.identifier)
		
		#mImages.append(find.identifier)
		imageList.append(images)

		print images
		print imageList
	ids = set(ids)
	return render_to_response("map.html",{"finds":all_finds, "imageList": imageList, "ids":ids})
