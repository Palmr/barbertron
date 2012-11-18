#!/usr/bin/env python
import subprocess
from pyechonest import config,track

config.ECHO_NEST_API_KEY="VZK0SNBGSEUD84U8S"

def generateControlFile(inputFile):
  controlFilename = "control-"+ str(datetime.now()) + ".txt"
  
  uploadedTrack = track.track_from_filename(filePath)
  audioKey = uploadedTrack.key
  audioKeyConfidence = uploadedTrack.key_confidence
  audioLength = uploadedTrack.seconds
  audioBarCount = uploadedTrack.bars.count()
  
  # generate chord progression
  with open(controlFilename, "w+") as controlFile:

    # test, go up in whole tones
    for t in xrange(0,10):
      controlFile.write("%f %i %i\n" % (t/2.0, 64 + 2 * t, 127 ))
  
  return controlFilename


def doBarberShopping(inputFile, outputFile):
  controlFilename = generateControlFile(inputFile)
  subprocess.call(["./barberism", "patch.pd", inputFile, controlFilename, outputFile])

