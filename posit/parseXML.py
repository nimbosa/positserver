from xml.dom import minidom

def getStringsFromXML(fileName):
	xmldoc = minidom.parse(fileName)
	print xmldoc.toxml()
	return xmldoc.getElementsByTagName('string')
