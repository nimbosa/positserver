from django.shortcuts import render_to_response
import sqlite3 as sqldb
from models import Image
from models import Find
from django.db.models import Q
from django import forms
from forms import *
from genXML import *
from DynForm import DynForm
from parseXML import *
import settings
import os
#global name, type, instances, server, record_name, instance_name
global valuesDict,kwargs,reflist, namesList, positDir, installationDir
valuesDict = {}
kwargs = {}
reflist = []
namesList = []
positDir = '/usr/share/POSIT'
installationDir = '/home/pgautam/positServer'
def home(request):
	appdata = "POSIT"
	appBody = """	
	This application has been designed to provide the user with the option to view
	the current status of their project, get data from the android device running 
	<a href="/">POSIT</a> via the <a href="/xml_rpc">xml-rpc interface</a> 
	<h3>Features</h3>
		<ul>
		<li> Create new application
		<ul>
		<li> with the previously generated xml files
		<li> with new xml files
		</ul>
		<li> View statistics
		</ul>
		"""
	return render_to_response("home.html",{"appdata":appdata,"appBody":appBody})


def images(request):
	all_images = Image.objects.all()
	return render_to_response("images.html",{"images":all_images})


def stats(request):
	all_finds= Find.objects.all()
	return render_to_response("stats.html",{"finds":all_finds})

def map(request):
	all_finds= Find.objects.all()
	print all_finds
	imageList = []
	ids = []
	for find in all_finds:
		images=Image.objects.filter(recordid=find.identifier)
		#imageDict[find.identifier] = images.
		#images = Images.objects.all()
		ids.append(find.identifier)
		
		#mImages.append(find.identifier)
		imageList.append(images)

		print images
		print imageList
	ids = set(ids)
	return render_to_response("map.html",{"finds":all_finds, "imageList": imageList, "ids":ids})

def appgen(request):
	if (request.method == 'POST') :
		form = AppgenForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['application_name']
			type = form.cleaned_data['application_type']
			instances = form.cleaned_data['instances']
			valuesDict["name"] = name;
			valuesDict["type"] = type;
			valuesDict["instances"] = instances;
			if instances == 'one':
				valuesDict['dbname']='posit-uni.db'
				return HttpResponseRedirect('/app/2/')
			else:
				valuesDict['dbname']='posit-multi.db'
				return HttpResponseRedirect('/app/3/')
	else:
		form = AppgenForm()
    	return render_to_response('appgen.html', {'form': form})

def appgen2(request):
	if (request.method == 'POST'):
		form = AppgenFormForRecord(request.POST)
		if form.is_valid():
			record_name = form.cleaned_data['record_name']
			server = form.cleaned_data['server_address']
			valuesDict["record_name"] = record_name;
			valuesDict["server"] = server;
			return HttpResponseRedirect('/app/4/')

	else :
		form = AppgenFormForRecord()
	
	return render_to_response('appgen.html', {'form': form})

def appgen3(request):
	global name, type, instances, server, record_name, instance_name
	if (request.method == 'POST'):
		form = AppgenFormForInstance(request.POST)
		if form.is_valid():
			record_name = form.cleaned_data['record_name']
			instance_name = form.cleaned_data['instance_name']
			server = form.cleaned_data['server_address']
			valuesDict["record_name"] = record_name;
			valuesDict["instance_name"] = instance_name;
			valuesDict["server"] = server;
			return HttpResponseRedirect('/app/4/')

	else :
		form = AppgenFormForInstance()
	
	return render_to_response('appgen.html', {'form': form})

def appgenfinal(request):
	global name, type, instances, server, record_name, instance_name,customized_by
	if (request.method == 'POST'):
		form = AppgenFormCredit(request.POST)
		if form.is_valid():
			customized_by = form.cleaned_data['customized_by']
			valuesDict["customized"] = customized_by
		saveEverything()
		copyXMLs()
		return HttpResponseRedirect('/dl/')

	else :
		form = AppgenFormCredit()
	
	return render_to_response('appgen.html', {'form': form})

def downloads(request):
	posit = '/downloads/POSIT.apk'
	pref = '/downloads/preferences.xml'
	strings ='/downloads/strings.xml'
	return render_to_response("downloads.html", {"posit":posit,"pref":pref,	 "strings":strings})

def copyXMLs():
	os.system("cp %s/tmp/res/raw/preferences.xml %s/downloads/"%(positDir,installationDir))
	os.system("cp %s/tmp/res/values/strings.xml %s/downloads/"%(positDir,installationDir))

def strings(request):
	if (request.method == 'POST'):
		form=DynForm(request.POST)
		form.setFields(kwargs)
		stringsDict = {}
		if form.is_valid():
			print "values"
			print namesList
			for k in namesList:
				stringsDict[k] = form.cleaned_data[k]
			saveStringsXML(stringsDict)
		return HttpResponseRedirect('/app/final/')
	else:
		reflist = getStringsFromXML('%s/posit/res/values/strings.xml'%positDir)
		for each in reflist:
			name = each.attributes["name"].value
			name= name.encode('ascii','ignore')
			if (name!="blankLabel"):
				print namesList
				namesList.append(name)
				kwargs[name] = forms.CharField(label=name, initial=each.firstChild.data)

		form = DynForm() # Create the form
		form.setFields(kwargs)

	return render_to_response('appgen.html', {'form': form})



def savePreferences(toplevel, values):
	file = open('%s/tmp/res/raw/preferences.xml'%positDir,'w')
	print values
	prefs = createXML(toplevel,values)
	file.write(prefs)
	file.close()

def saveStringsXML(values):
	file = open ('%s/tmp/res/values/strings.xml'%positDir,'w')
	file.write('<?xml version="1.0" encoding="utf-8"?>\n')
	xmlstring = createStringsXML(values)
	print xmlstring
	file.write(xmlstring)
	file.close()


def saveEverything():
	savePreferences('application', valuesDict)
	createAPK()

def generateDBInfo():
	dbInfo = {}
	

def imageMagickLogo():
	genCommand = """convert logo.jpg  -font Arial -pointsize 20 \
            -draw \"gravity south \
                   fill black  text 0,12 'Copyright' \
                   fill white  text 1,11 'Copyright' \" \
            wmark_text_drawn.jpg"""


def createAPK():
	print "here"
	os.system("cd %s/tmp/;ant ; mv bin/POSIT.apk %s/downloads/"%(positDir,installationDir))
