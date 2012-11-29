#!/usr/bin/env python
import sys, traceback, cgi
from barberlogging import BarberLogging

try:
	inputs = cgi.FieldStorage()
	barbershoppedFile = str(inputs['file'].value)

	twimlResponse = '<?xml version="1.0" encoding="UTF-8" ?>\n<Response>\n<Play>' + barbershoppedFile + '</Play>\n</Response>'

	logger = BarberLogging('log_playback.log', 'playback.py')
	logger.log(twimlResponse)

	print('Content-type: text/xml\n')
	print(twimlResponse)
except:
	logger = BarberLogging('log_playback.log', 'playback.py - Error')
	logger.log(traceback.format_exc())

	print('Content-type: text/plain\n')
	print('Error:\n')
	print(traceback.format_exc())