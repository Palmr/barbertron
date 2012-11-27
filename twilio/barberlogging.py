import sys, time

class BarberLogging():
	def __init__(self, loggingFile, loggingConsumer):
		self.errlog = open(loggingFile, 'a')
		self.consumer = loggingConsumer

	def log(self, debugData):
		errtime = '--- ' + time.ctime(time.time()) + ' [' + self.consumer + '] ---\n'
		self.errlog.write(errtime)
		self.errlog.write(debugData + '\n')

if __name__ == '__main__':
	testLogger = BarberLogging('log-test.txt', 'testing')
	testLogger.log('Hello World')