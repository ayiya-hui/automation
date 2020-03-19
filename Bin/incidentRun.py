import incidentHandler
import createQuery
import parseReturn
import time
import verifyResult
import createDevice
import logging

PATTERN_BASE="clear conditions are met"
TIME_BASE="rule does not trigger for $n minutes"

def RunTask(config, testSuite):
	option=config['option']
	myIncident=incidentHandler.incidentHandler(config['dataCollector'], config['appServer'], config['user'], config['password'])
	myIncident.udpClient()
	totalParam=[]
	type=testSuite.type
	reason=''
	if type=='pattern':
		reason=PATTERN_BASE

	if type=='time':
		reason=TIME_BASE

	for testcase in testSuite.testcaseList:
		#create device in CMDB for testing then wait 2 minutes for it to work
		if testcase.createDevice=="yes":
			createDevice.createDeviceList(config['appServer'], testcase.deviceType, testcase.deviceName, testcase.reporter, 1, "1")
			time.sleep(120)

		if option=="check":
			myParam={}
			myParam['firstCount']='1'
			myParam['secondCount']=testcase['repeatCount']

			if type=='time':
				myTime=(int(testcase.clearInterval)-300)/60
				num=str(myTime)
				reason.replace("$n", num)

			myParam['reason']=reason

			queryString='eventType IN ("'+testcase.eventType+'") AND hostIpAddr IN ('+testcase.reporter+')'
			queryXML=createQuery.CreateQueryXML(queryString, 'Incidents', '1')
			logging.debug(queryXML)

		if testSuite.sendEvent=="true":
			incidentEvent=testcase.incidentEvent
			for i in range(int(incidentEvent.repeatCount)):
				for j in range(int(incidentEvent.sendCount)):
					for msg in incidentEvent.incidentList:
						myIncident.sendEvent(msg)
					time.sleep(int(incidentEvent.sendInterval))
				time.sleep(int(incidentEvent.repeatInterval))
				if option=="check":
					myIncident.getEvent(queryXML)
					myParam["Event "+str(i+1)]=parseReturn.XMLParsingQueryResult(myIncident.xml)

		#clear event
		if testSuite.clearEvent=="true":
			time.sleep(int(testcase.clearInterval))
			myIncident.sendEvent(testcase.clearEvent)

		if testSuite.type!="general" and option=="check":
			time.sleep(int(testcase.clearWait))
			myIncident.getEvent(queryXML)
			myParam["Clear Event"]=parseReturn.XMLParsingQueryResult(myIncident.xml)

		if option=="check":
			logging.debug(myParam)
			totalParam.append(myParam)

			for param in totalParam:
				verifyResult.verifyResult(param)

			finalResult="good"
		else:
			finalResult="test done"

	myIncident.udpClientClose()
	return finalResult
