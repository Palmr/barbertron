#!/usr/bin/env python
import cgi
import urllib
import time
import random
from twilio.rest import TwilioRestClient
from barbershop import doBarberShopping
from toSoundcloud import postSoundcloud

ACCOUNT_SID = "AC4da27eb5c20276bef4fd14f5e8f8856b"
AUTH_TOKEN = "044600f3d19bf476462555ee120cd7a5"
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

inputs = cgi.FieldStorage()

baseURL = "http://86.6.44.109/";
barbershopID = "%i_%i" % (int(time.time() * 1e4), int(random.random() * 1e6))
originalAudioFile = "originalAudio_" + barbershopID + ".wav"
barbershoppedAudioFile = "barbershoppedAudio_" + barbershopID + ".wav"

print("Content-type: text/plain\n\n")

with open("/var/www/cgi-bin/music-hack-day/log_" + barbershopID + ".log","w+") as logFile:
  logFile.write("HEADERS:\n ")
  logFile.write(str(inputs))

# Parameters
# RecordingUrl 	the URL of the recorded audio
# RecordingDuration 	the duration of the recorded audio (in seconds)
# Digits 	the key (if any) pressed to end the recording or 'hangup' if the caller hung up

# Parse the inputs
audioURL = str(inputs['RecordingUrl'].value)
callerNumber = str(inputs['Caller'].value)

# Download the recording
urllib.urlretrieve(audioURL, originalAudioFile)

# Do-barbershopping
doBarberShopping(originalAudioFile, '../../html/'+barbershoppedAudioFile, barbershopID)

# Post response back to twilio
# respond with the xml pointing barbershoppedAudioFile back to the original number that called
playbackURL = baseURL + "/cgi-bin/music-hack-day/playback.py?file=" + baseURL + barbershoppedAudioFile
call = client.calls.create(to=callerNumber, from_="+442071839808", url=playbackURL)

# Upload to soundcloud
soundcloudURL = postSoundcloud(barbershopID, "../../html/" + barbershoppedAudioFile)

message = client.sms.messages.create(to=callerNumber, from_="+442071839808",
                                     body="Nice singing! " + soundcloudURL)
