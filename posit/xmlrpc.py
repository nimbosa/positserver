# Patchless XMLRPC Service for Django
# Kind of hacky, and stolen from Crast on irc.freenode.net:#django
# Self documents as well, so if you call it from outside of an XML-RPC Client
# it tells you about itself and its methods
# Thanks to:
# Brendan W. McAdams <brendan.mcadams@thewintergrp.com>

# SimpleXMLRPCDispatcher lets us register xml-rpc calls w/o
# running a full XMLRPC Server.  It's up to us to dispatch data
from django.shortcuts import render_to_response
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.db import connection
from models import *
import settings
# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None) # Python 2.5

def save_find(Name, Identifier, Description, Latitude, Longitude,Age, Sex, Tagged, Time):
    """saves the finds sent over xmlrpc to the database"""
    if (Tagged==1):
        tagBool = True
    else:
        tagBool = False
    f = Find(name=Name, identifier=str(Identifier), description=Description,
             latitude=float(Latitude), longitude=float(Longitude), age=Age, sex=Sex, tagged=tagBool, time=Time)
    f.save()
    print f
    return 1

def save_instance(name, description, latitude, longitude,rowId):
    """
    Saves the instances sent over xmlrpc
    """
    pass

def save_image(file,name,id,desc):
    """
    Saves the images sent over xmlrpc
    """
    global connection
    datum = file.data
    print datum
    #filename = 'pic%s%d.png'%(name,id)
    fileName = name
    print fileName
    fileLocation = settings.MEDIA_ROOT+'/images/'+fileName
    thefile = open(fileLocation, "wb")
    thefile.write(datum)
    thefile.close()
    i = Image(filename=fileName,recordid_id=id,description=desc)
    i.save()
    print filename+" saved"
    return 1

'''Needs to go into a different class/file'''
def save_to_db(filename,id):
    connection =sqlite3.connect('/home/pgautam/positServer/database/db',isolation_level=None)
    execstring = "insert into posit_images (filename, recordid) values (%s,%d)"%filename%id
    print execstring
    connection.execute(execstring)
    connection.commit()
    connection.close()


# Register a function under a different name
def adder_function(x,y):
    """    Adds two numbers    """
    return x + y

def return_array():
    """
    Returns an array, useful for testing
    """
    response = [ "server : val 1", "server: val 2", "server: val 3"]
    return response

def show_data(data):
    """
    Prints back whatever you send to the server 
    """
    return data
 

def rpc_handler(request):
    """
    the actual handler:
    if you setup your urls.py properly, all calls to the xml-rpc service
    should be routed through here.
    If post data is defined, it assumes it's XML-RPC and tries to process as such
    Empty post assumes you're viewing from a browser and tells you about the service.
    """

    response = HttpResponse()
    if len(request.POST):
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        
        string = "<b>This is an XML-RPC Service.</b><br>"
        string +="You need to invoke it using an XML-RPC Client!<br>"
        string +="The following methods are available:<ul>"
        methods = dispatcher.system_listMethods()

        for method in methods:
            # right now, my version of SimpleXMLRPCDispatcher always
            # returns "signatures not supported"... :(
            # but, in an ideal world it will tell users what args are expected
            sig = dispatcher.system_methodSignature(method)

            # this just reads your docblock, so fill it in!
            help =  dispatcher.system_methodHelp(method)

            string+= "<li><b>%s</b>: %s" % (method, help)
        string+="</ul>"
    return render_to_response("xmlrpc.html",{"appBody":string})

def multiply(a, b):
    """
    Multiplication is fun!
    Takes two arguments, which are multiplied together.
    Returns the result of the multiplication!
    """
    return a*b

# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from the XML-RPC side...
dispatcher.register_function(multiply, 'multiply')
#dispatcher.register_function(get_data,'info');
dispatcher.register_function(return_array, 'test')
dispatcher.register_function(show_data,'echo')
dispatcher.register_function(save_image,'saveImage')
dispatcher.register_function(save_find,'saveFind')
dispatcher.register_function(save_instance,'saveInstance')
#dispatcher.register_introspection_functions()