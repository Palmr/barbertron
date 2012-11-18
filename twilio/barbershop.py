#!/usr/bin/env python
import subprocess
from pyechonest import config,track

config.ECHO_NEST_API_KEY="VZK0SNBGSEUD84U8S"

def generateControlFile(inputFile, barbershopID):
  controlFilename = "control-"+ barbershopID + ".txt"
  
  uploadedTrack = track.track_from_filename(inputFile)
  audioKey = uploadedTrack.key
  audioKeyConfidence = uploadedTrack.key_confidence
  #audioBarCount = uploadedTrack.bars.count()
  
  # generate chord progression
  with open(controlFilename, "w+") as controlFile:

    # test, go up in whole tones
    for t in xrange(1,4):
      controlFile.write("%f %i %i\n" % (t*2.0, 54 + 3 * t, 117 ))
      controlFile.write("%f %i %i\n" % (t*2.0, 59 + 3 * t, 117 ))
      controlFile.write("%f %i %i\n" % (t*2.0, 64 + 3 * t, 117 ))
  
  return controlFilename


def doBarberShopping(inputFile, outputFile, barbershopID):
  controlFilename = generateControlFile(inputFile, barbershopID)
  subprocess.call(["./barberism", "./patch.pd", inputFile, controlFilename, outputFile])

