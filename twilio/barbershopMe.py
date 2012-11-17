#!/usr/bin/env python
import cgi

#import cgitb
#cgitb.enable()

import datetime
inputs = cgi.FieldStorage()


with open("log_"+ str(datetime.now()) + ".log","w") as logFile:
  logFile.write(str(inputs))


# Parameters

# RecordingUrl 	the URL of the recorded audio
# RecordingDuration 	the duration of the recorded audio (in seconds)
# Digits 	the key (if any) pressed to end the recording or 'hangup' if the caller hung up

audioURL = inputs['RecordingURL']

localAudioFile = "testAudio_" + str(datetime.now()) + ".wav"
urllib.urlretrieve(audioURL, localAudioFile)

print ("Retrieved " + audioURL + "\n")
