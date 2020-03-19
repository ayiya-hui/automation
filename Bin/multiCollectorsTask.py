import logging
import autoTestClass
import ComHandler
import os

def runMultiCollectors(id, config, testSuite):
    collectors=config['dataCollector'].split(",")
    duration=int(config['duration'])
    for i in range(duration):
        for collector in collectors:
            collectInfo=collector.split(":")
            collectorIP=collectInfo[0]
            hostBase=collectInfo[1]
            hosts=hostBase.split(".")
            lastAddr=int(hosts[-1])+int(id)
            hosts[-1]=str(lastAddr)
            host='.'.join(hosts)

            if testSuite.method=='snmptrap':
                for case in testSuite.testcases:
                   event1=''
                   if '$localhost' in case.parseEvent:
                       event1=case.parseEvent.replace("$localhost", config["localhost"])
                   else:
                       event1=case.parseEvent
                   if '$dataCollector' in event1:
                       event2=case.parseEvent.replace("$dataCollector", collectorIP )
                   else:
                       event2=event1
                   logging.debug(event2)
                   returnC=os.system(event2)
            else:
                myHandler=ComHandler.comHandler(collectorIP, config['appServer'], config['user'], config['password'])
                myHandler.udpClient()
                for case in testSuite.testcases:
                    if '$reporter' in case.parseEvent:
                        sentEvent=case.parseEvent.replace("$reporter", host)
                    else:
                        sentEvent=case.parseEvent
                    myHandler.sendEvent(sentEvent)
                    logging.debug(sentEvent)
                myHandler.udpClientClose()
        i+=1

    return None



