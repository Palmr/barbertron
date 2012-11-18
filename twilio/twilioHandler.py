#!/usr/bin/env python
import cgi
import urllib
from datetime import datetime

inputs = cgi.FieldStorage()

baseURL = "http://86.6.44.109/cgi-bin/music-hack-day/";
timestampNow = str(datetime.now()).replace(' ', '_')
originalAudioFile = "originalAudio_" + timestampNow + ".wav"
barbershoppedAudioFile = "barbershoppedAudio_" + timestampNow + ".wav"

print("Content-type: text/plain\n\n")

with open("/var/www/cgi-bin/music-hack-day/log_"+ timestampNow + ".log","w+") as logFile:
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
# doBarberShopping(originalAudioFile, barbershoppedAudioFile)

# Post response back to twilio
# respond with the xml pointing barbershoppedAudioFile back to the original number that called
playbackURL = baseURL + "playback.py?file=" + barbershoppedAudioFile

