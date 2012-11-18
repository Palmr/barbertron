#!/usr/bin/env python
import cgi
import urllib
from barbershop import doBarberShopping

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
doBarberShopping(originalAudioFile, '../../html/'+barbershoppedAudioFile)

# Post response back to twilio
# respond with the xml pointing barbershoppedAudioFile back to the original number that called
playbackURL = baseURL + "playback.py?file=" + baseURL + barbershoppedAudioFile
# post to the call method passing our number, callerNumber and the playbackURL
