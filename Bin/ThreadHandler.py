import threading
import generalRun
import logging
import time

class autoTestThread(threading.Thread):
	vlock=threading.Lock()
	results=[]
	def __init__ (self, id, config, testSuite):
		self.id=id
		self.config=config
		self.testSuite=testSuite
		threading.Thread.__init__(self)

	def getResult(self):
		return self.results

	def run (self):
		print "Running Test Suite %s with %s" % (self.testSuite.name, self.name)
		logging.debug("Running Test Suite %s with %s" % (self.testSuite.name, self.name))
		testreturn=generalRun.RunTask(self.id, self.config, self.testSuite)
		if testreturn!=None:
			self.vlock.acquire()
			self.results.append(testreturn)
			self.vlock.release()







