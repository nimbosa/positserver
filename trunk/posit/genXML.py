from xml.dom.minidom import Document

def createXML(topLevel, values):
	doc = Document()
	app = doc.createElement(topLevel)
	doc.appendChild(app)
	for k, v in values.items():
		x = doc.createElement(k)
		x.appendChild(doc.createTextNode(v))
		app.appendChild(x)
	return app.toprettyxml()

def createStringsXML(values):
	doc = Document()
	app = doc.createElement('resources')
	doc.appendChild(app)
	for k, v in values.items():
		x = doc.createElement('string')
		x.setAttribute("name",k)
		x.appendChild(doc.createTextNode(v))
		app.appendChild(x)
	return app.toprettyxml()

