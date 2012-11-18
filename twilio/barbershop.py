#!/usr/bin/env python
import os
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
    controlFile.write("Some series of notes based of the key/seconds/bar count...\n")
  
  return controlFilename


def doBarberShopping(inputFile, outputFile):
  controlFilename = generateControlFile()
  os.system("barberism patch.pd " + inputFile + " " + controlFilename + " " + outputFile)

