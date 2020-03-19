from testClass import testSuite, testCase
import time

class incidentSuite(testSuite):
    def __init__(self):
        testSuite.__init__(self)
        self.data=''
        self.runStatus=''

class incidentCase(testCase):
    def __init__(self):
        testCase.__init__(self)
        self.repeatCount=''
        self.events=''
        self.wait=''
        self.clearType=''

    def runAggregateIncident(self, option, method, preData):
        self.__fillin(preData)
        myRet, myData=self.runIncident(option, method, aggregate=preData['incidentId'])

        return myRet, myData

    def runClearIncident(self, option, method, preData):
        self.__fillin(preData)
        myData={}
        if self.clearType=='condition':
            myRet, myData=self.runIncident(option, method, aggregate=preData['incidentId'])
        elif self.clearType=='time':
            time.sleep(60*(int(self.wait)-10))
            myRet=self.queryIncident(advance=preData['incidentId'])
            if self.resultData:
                myData=self.resultData
            else:
                myData={}
        return myRet, myData

    def __fillin(self, preData):
        for key in self.parameters.keys():
            if self.parameters[key].lower()=='any':
                self.parameters[key]=preData[key]

class incidentEvent:
    def __init__(self):
        self.incidentMsg=''


