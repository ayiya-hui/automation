import ThreadHandler
import testReportHandler

def TestRun(config, testSuites):
	threads=[]
	id=1
	for testSuite in testSuites.suites:
		thread=ThreadHandler.autoTestThread(id, config, testSuite)
		thread.start()
		threads.append(thread)
		id+=1

	for thread in threads:
		thread.join()

	fullResult=thread.results
	print "Main Test Thread Exiting"

	if len(fullResult)==0:
		print "No result returned. Exit."
		if config['option']=="SendOnly":
		    msg="SendOnly option selected. Successful send."
		else:
		    msg="Compare result return NONE. Check log for problem."
	else:
		myReport=testReportHandler.testReport()
		msg=myReport.generateReport(config, fullResult)

	return msg
