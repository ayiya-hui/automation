import logDiscoveryTask
import multiCollectorsTask
#import linuxFileMonitorTask
#import eventExportTask
#import RBACTask
#import reportTask
#import eventTypeTask
import TestTask

def RunTask(id, config, testSuite):
	if config['testTask']=="logDiscovery":
		finalResult=logDiscoveryTask.runLogDiscovery(config, testSuite)
	elif config['testTask']=="multiCollectors":
		finalResult=multiCollectorsTask.runMultiCollectors(id, config, testSuite)
	#elif config['testTask']=="linuxFileMonitor":
	#	finalResult=linuxFileMonitorTask.runLinuxFileMonitor(config, testSuite)
	#elif config['testTask']=="eventExport":
	#	finalResult=eventExportTask.runEventExport(config, testSuite)
	#elif config['testTask']=="RBAC":
	#	finalResult=RBACTask.runRBAC(config, testSuite)
	#elif config['testTask']=="report":
	#	finalResult=reportTask.runReport(config, testSuite)
	#elif config['testTask']=="eventType":
	#	finalResult=eventTypeTask.runEventType(config, testSuite)
	else:
		finalResult=TestTask.runTest(config, testSuite)

	return finalResult

