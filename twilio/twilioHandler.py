#!/usr/bin/env python
import cgi
import urllib
import time
import random
from twilio.rest import TwilioRestClient
from barbershop import doBarberShopping
from toSoundcloud import postSoundcloud
from secrets import twilioSecrets,serverSecrets

twilioClient = TwilioRestClient(twilioSecrets['SID'], twilioSecrets['TOKEN'])

inputs = cgi.FieldStorage()

barbershopID = "%i_%i" % (int(time.time() * 1e4), int(random.random() * 1e6))

baseURL = "http://" + serverSecrets['IP'] + "/";

defaultWebDirectory = "/var/www/html/"
originalAudioFile = "originalAudio_" + barbershopID + ".wav"
barbershoppedAudioFile = "barbershoppedAudio_" + barbershopID + ".wav"

print("Content-type: text/plain\n\n")

with open(defaultWebDirectory + "log_" + barbershopID + ".log", "w+") as logFile:
  logFile.write("HEADERS:\n ")
  logFile.write(str(inputs))

# Parse the inputs
audioURL = str(inputs['RecordingUrl'].value)
callerNumber = str(inputs['Caller'].value)

# Download the recording
urllib.urlretrieve(audioURL, defaultWebDirectory + originalAudioFile)

# Do-barbershopping
doBarberShopping(defaultWebDirectory + originalAudioFile, defaultWebDirectory + barbershoppedAudioFile, barbershopID)

# Post response back to twilio
# respond with the xml pointing barbershoppedAudioFile back to the original number that called
playbackURL = baseURL + "/cgi-bin/music-hack-day/playback.py?file=" + baseURL + barbershoppedAudioFile
twilioCall = twilioClient.calls.create(to=callerNumber, from_="+442071839808", url=playbackURL)

# Upload to soundcloud
soundcloudURL = postSoundcloud(barbershopID, defaultWebDirectory + barbershoppedAudioFile)
twilioSMS = twilioClient.sms.messages.create( to=callerNumber, from_="+442071839808",
                                              body="Nice singing! " + soundcloudURL)
