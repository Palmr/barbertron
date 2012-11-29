#!/usr/bin/env python
import subprocess
import math
from pyechonest import config,track
from secrets import echoNestSecrets
from barberlogging import BarberLogging

config.ECHO_NEST_API_KEY = echoNestSecrets['API_KEY']

class Barbershopper():
	def __init__(self, barbershopID, logger = BarberLogging('log_barbershop.log', 'Barbershopper')):
		self.barbershopID = barbershopID
		self.logger = logger

	def generateControlFile(self, inputFile):
		controlFilename = 'control-' + self.barbershopID + '.txt'
		self.logger.log('Control file for barbershopping: ' + controlFilename)

		# Upload original audio to The Echo Nest for analysis
		uploadedTrack = track.track_from_filename(inputFile)
		self.logger.log('Echo nest says original tack duration is ' + str(uploadedTrack.duration))
		self.logger.log('Echo nest says original tack in key: ' + str(uploadedTrack.key) + ' (confidence: ' + str(uploadedTrack.key_confidence) + ')')
		track_length = math.floor(uploadedTrack.duration)
		key_offset = uploadedTrack.key - 6
		
		# Generate chord progression
		with open(controlFilename, 'w+') as controlFile:
			# Come up with a good algorithm here later...
			controlFile.write("%f %i %i\n" % (0.000001, key_offset + 60, 117))
			controlFile.write("%f %i %i\n" % (0.000001, key_offset + 64, 117))
			controlFile.write("%f %i %i\n" % (0.000001, key_offset + 67, 117))
			controlFile.write("%f %i %i\n" % (0.000001, key_offset + 71, 117))
			for t in xrange(1, track_length/2):
				controlFile.write("%f %i %i\n" % (t * 2.0, key_offset + 60 + t + key_offset, 117))
				controlFile.write("%f %i %i\n" % (t * 2.0, key_offset + 64 + t + key_offset, 117))
				controlFile.write("%f %i %i\n" % (t * 2.0, key_offset + 67 + t + key_offset, 117))
				controlFile.write("%f %i %i\n" % (t * 2.0, key_offset + 71 + t + key_offset, 117))

		return controlFilename

	def doBarberShopping(self, inputFile, outputFile):
		controlFilename = self.generateControlFile(inputFile)
		self.logger.log('Barbershopping ' + inputFile + ' into ' + outputFile)
		subprocess.call(['./barberism', './patch.pd', inputFile, controlFilename, outputFile])

if __name__ == '__main__':
	bshop = Barbershopper('xxxtestxxx')
	bshop.doBarberShopping('barbershop-star-solo2.wav', 'barbershop-star-solo2-output.wav')
