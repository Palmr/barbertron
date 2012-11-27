#!/usr/bin/env python
import subprocess
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
		key_offset = uploadedTrack.key - 6
		self.logger.log('Echo nest says original tack in key: ' + str(uploadedTrack.key))
		
		# Generate chord progression
		with open(controlFilename, 'w+') as controlFile:
			# Come up with a goold algorithm here later...
			for t in xrange(1,4):
				controlFile.write("%f %i %i\n" % (t*2.0, key_offset + 54 + 3 * t, 117 ))
				controlFile.write("%f %i %i\n" % (t*2.0, key_offset + 59 + 3 * t, 117 ))
				controlFile.write("%f %i %i\n" % (t*2.0, key_offset + 64 + 3 * t, 117 ))

		return controlFilename

	def doBarberShopping(self, inputFile, outputFile):
		controlFilename = self.generateControlFile(inputFile)
		self.logger.log('Barbershopping ' + inputFile + ' into ' + outputFile)
		subprocess.call(['./barberism', './patch.pd', inputFile, controlFilename, outputFile])

#if __name__ == '__main__':
  #bshop = Barbershopper('xxtestxx')
	#bshop.doBarberShopping('test.wav', 'test-output.wav')
