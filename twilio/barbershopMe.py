#!/usr/bin/env python
import cgi
import urllib

#import cgitb
#cgitb.enable()

from datetime import datetime
inputs = cgi.FieldStorage()

print("Content-type: text/plain\n\n")

with open("/var/www/cgi-bin/music-hack-day/log_"+ str(datetime.now()) + ".log","w+") as logFile:
  logFile.write("HEADERS:\n ")
  logFile.write(str(inputs))

# Parameters
# RecordingUrl 	the URL of the recorded audio
# RecordingDuration 	the duration of the recorded audio (in seconds)
# Digits 	the key (if any) pressed to end the recording or 'hangup' if the caller hung up

audioURL = str(inputs['RecordingUrl'].value)

localAudioFile = "testAudio_" + str(datetime.now()) + ".wav"
urllib.urlretrieve(audioURL, localAudioFile)

print ("Retrieved " + audioURL + "\n")
