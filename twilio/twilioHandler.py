#!/usr/bin/env python
import cgi
import urllib
import time
import random
import traceback
from twilio.rest import TwilioRestClient
from barbershop import Barbershopper
from toSoundcloud import postSoundcloud
from secrets import twilioSecrets,serverSecrets
from barberlogging import BarberLogging

logFile = 'log_twilio.log'
logger = BarberLogging(logFile, 'twilioHandler.py')

try:
	twilioClient = TwilioRestClient(twilioSecrets['SID'], twilioSecrets['TOKEN'])

	# Parse the inputs
	inputs = cgi.FieldStorage()
	audioURL = str(inputs['RecordingUrl'].value)
	callerNumber = str(inputs['Caller'].value)
	logger.log('Call recieved from (' + callerNumber + ') giving a recording url of: ' + audioURL)

	# Set up vars
	barbershopID = "%i_%i" % (int(time.time() * 1e4), int(random.random() * 1e6))
	baseURL = "http://" + serverSecrets['IP'] + "/";
	defaultWebDirectory = "/var/www/html/"
	originalAudioFile = "originalAudio_" + barbershopID + ".wav"
	barbershoppedAudioFile = "barbershoppedAudio_" + barbershopID + ".wav"

	# Download the recording
	urllib.urlretrieve(audioURL, defaultWebDirectory + originalAudioFile)
	logger.log('Downloaded ' + audioURL + ' to ' + defaultWebDirectory + originalAudioFile)

	# Do-barbershopping
	bshop = Barbershopper(barbershopID, logger)
	bshop.doBarberShopping(defaultWebDirectory + originalAudioFile, defaultWebDirectory + barbershoppedAudioFile)
	logger.log('File barbershopped, result: ' + defaultWebDirectory + barbershoppedAudioFile)

	# Post response back to twilio
	# respond with the xml pointing barbershoppedAudioFile back to the original number that called
	playbackURL = baseURL + "/cgi-bin/music-hack-day/playback.py?file=" + baseURL + barbershoppedAudioFile
	twilioCall = twilioClient.calls.create(to=callerNumber, from_=twilioSecrets['PHONE_NUMBER'], url=playbackURL)
	logger.log('Calling (' + callerNumber + ') from (' + twilioSecrets['PHONE_NUMBER'] + ')')

	# Upload to soundcloud
	soundcloudURL = postSoundcloud(barbershopID, defaultWebDirectory + barbershoppedAudioFile)
	logger.log('Uploaded to soundcloud: ' + soundcloudURL)
	twilioSMS = twilioClient.sms.messages.create( to=callerNumber, from_=twilioSecrets['PHONE_NUMBER'], body="Nice singing! " + soundcloudURL)
	logger.log('Sending soundcloud link via SMS to (' + callerNumber + ') from (' + twilioSecrets['PHONE_NUMBER'] + ')')

	print('Content-type: text/plain\n')
	print('Recording barbershopped :)')
except:
	logger = BarberLogging(logFile, 'twilioHandler.py - Error')
	logger.log(traceback.format_exc())

	print('Content-type: text/plain\n')
	print('Error:\n')
	print(traceback.format_exc())

