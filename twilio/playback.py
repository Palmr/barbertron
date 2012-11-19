#!/usr/bin/env python
import cgi

inputs = cgi.FieldStorage()
barbershoppedFile = str(inputs['file'].value)

print("Content-type: text/xml\n\n<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<Response>\n<Play>"+barbershoppedFile+"</Play>\n</Response>")

