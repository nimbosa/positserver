#!/usr/bin/env python2.5
'''
    positServer: An application to interface with the POSIT application 
    I developed for my project on Google Android
    Copyright (C) 2008  Prasanna Gautam
    pythonxml.py:
     This program exposes the xmlrpc communication procedures for sending 
     and receiving files between Android and the server

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import socket
import fcntl
import struct
#import MySQLdb
import cPickle
import xmlrpclib
from base64 import b64encode
import sqlite3

global server
global connection

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
    s.fileno(),
    0x8915,  # SIOCGIFADDR
    struct.pack('256s', ifname[:15])
    )[20:24])

def create_server():
    global server
    # Create server
    ipaddress = get_ip_address('eth0')
    port = 8000
    server = SimpleXMLRPCServer((ipaddress, port))
    print "Server running at "+ipaddress+" on port "+str(port)
    server.register_introspection_functions()

def save_finds(identifier, description, type, latitude, longitude):
    global connection
    print identifier, description, type, latitude, longitude
    execstring = "insert into posit_finds (identifier, description, latitude, longitude,type) values (\'%s\',\'%s\', %f, %f, \'%s\')"%(str(identifier),description, float(latitude), float(longitude), type)
    print connection, execstring
    connection.execute(execstring)
    connection.commit()
    return 1


def save_file(file,name,id):
    global connection
    datum = file.data
    print datum
    #filename = 'pic%s%d.png'%(name,id)
    filename = name
    print filename
    filelocation = '/home/pras/positServer/media/images/'+filename
    thefile = open(filelocation, "wb")
    thefile.write(datum)
    thefile.close()
    execstring = "insert into posit_images (filename, recordid) values (\'%s\',%d)"%(filename,id)
    connection.execute(execstring)
    connection.commit()
    print filename+" saved"
    return 1

'''Needs to go into a different class/file'''
def save_to_db(filename,id):
    connection =sqlite3.connect('/home/pras/positServer/database/db',isolation_level=None)
    execstring = "insert into posit_images (filename, recordid) values (%s,%d)"%filename%id
    print execstring
    connection.execute(execstring)
    connection.commit()
    connection.close()


# Register a function under a different name
def adder_function(x,y):
    return x + y

def return_array():
    response = [ "server : val 1", "server: val 2", "server: val 3"]
    return response

def show_data(data):
    print data


#connect to the MySQL server
def get_data():
    db = MySQLdb.connect("127.0.0.1", "root", "lamo", "posit")
    c= db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT id, latitude, longitude, description FROM db")
    arr = []
    result_set=c.fetchall()
    for row in result_set:
        #arr.append(xmlrpclib.Binary(row[0]))
        #print row
        entry = []
        entry.append(row["id"])
        entry.append(row["latitude"])
        entry.append(row["longitude"])
        entry.append(row["description"])
        #entry.append(cPickle.dumps(row["photo"]))
        arr.append(entry)
    db.close();
    # this is pretty much what is being sent!!
    #print xmlrpclib.dumps(result_set)
    return arr;

if __name__=='__main__':
    create_server()
    server.register_function(get_data,'info');
    server.register_function(return_array, 'test')
    server.register_function(adder_function, 'add')
    server.register_function(show_data,'showdata')
    server.register_function(save_file,'savefile')
    server.register_function(save_finds,'saveFinds')
    # Run the server's main loop
    server.register_instance(MyFuncs())
    server.serve_forever()

if __name__=='__init__':
    connection =sqlite3.connect('/home/pras/positServer/database/db',isolation_level=None)

