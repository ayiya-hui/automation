import restApiDataHandler

class ruleHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.allRules=self.__getAllRules()

    def __getAllRules(self):
        myRest=restApiDataHandler.restApiDataHandler(self.appServer)
        ruleMap=myRest.getData('rule')

        return ruleMap

    def getRulebyId(self, incident_type):
        myRule=''
        for id in self.allRules.keys():
            if self.allRules[id].incidentType.split('EventType$')[-1]==incident_type:
                myRule=self.allRules[id]
                break
        if not myRule:
            print 'Rule IncidentId %s not exist in system.' % incident_type

        return myRule

    def getRulebyName(self, name):
        myRule=''
        for id in self.allRules.keys():
            if self.allRules[id].name==name:
                myRule=self.allRules[id]
                break
        if not myRule:
            print 'Rule name %s not exist in system.' % name

        return myRule




