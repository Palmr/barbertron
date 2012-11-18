#!/usr/bin/env python
import cgi
import urllib

from barbershop import doBarberShopping

#import cgitb
#cgitb.enable()

inputs = cgi.FieldStorage()

print("Content-type: text/plain\n\n")

barbershopID = "%i_%i" % (int(time.time() * 1e4), int(random.random() * 1e6))

with open("/var/www/cgi-bin/music-hack-day/log_" + barbershopID + ".log","w+") as logFile:
  logFile.write("HEADERS:\n ")
  logFile.write(str(inputs))

# Parameters
# RecordingUrl 	the URL of the recorded audio
# RecordingDuration 	the duration of the recorded audio (in seconds)
# Digits 	the key (if any) pressed to end the recording or 'hangup' if the caller hung up

audioURL = str(inputs['RecordingUrl'].value)

localAudioInputFile = "audioInput_" + barbershopID + ".wav"
localAudioOutputFile = "audioOutput_" + barbershopID + ".wav"

urllib.urlretrieve(audioURL, localAudioInputFile)

print ("Retrieved " + audioURL + "\n")

doBarberShopping(localAudioInputFile, localAudioOutputFile)

print("Processed; saved to " + localAudioOutputFile)
