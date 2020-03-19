class dataCompareHandler:
    def __init__(self, expect, actual):
        self.expect=expect
        self.actual=actual
        self.result=''
        self.passed=[]
        self.failed=[]
        self.missed=[]
        self.improved=[]

    def compare(self):
        comKey=[key for key in self.expect.keys() if key in self.actual.keys()]
        missKey=[key for key in self.expect.keys() if key not in self.actual.keys()]
        improveKey=[key for key in self.actual.keys() if key not in self.expect.keys()]
        if len(missKey)!=0:
            self.result='Miss'
            for key in missKey:
                self.missed

    def __compareList(self):
        pass

    def __compareHash(self):
        pass

class param:
    def __init__(self):
        self.name=''
        self.expect=''
        self.actual=''

class output:
    def __init__(self):
        self.result={}
        self.errorString=''

    def output(self, oldData, newData, db=False):
        for id in oldData.keys():
            if id in newData.keys():
                myoldData=oldData[id]
                mynewData=newData[id]
                myName=mynewData['Name']
                if str(myoldData).replace(" ", "")!=str(mynewData).replace(" ", ""):
                    self.errorString+='\nid: '+id+' name: '+myName+': Not Match'+'\n'+str(myoldData)+'\n'+str(mynewData)
                    for name in myoldData.keys():
                        self.compare(name, myoldData[name], mynewData[name])
                    self.result[id]=myName

    def compare(self, name, old, new):
        if old!=new:
            type=getType(old)
            if type=='dict':
                for subName in old.keys():
                    if subName in new.keys():
                        if old[subName]!='' and new[subName]!='':
                            self.compare(subName, old[subName], new[subName])
            elif type=='list':
                for item in old:
                    for key in new:
                        for myKey in KEYS:
                            if myKey in item['attribute'].keys():
                                if item['attribute'][myKey]==key['attribute'][myKey]:
                                    self.compare(name, item, key)
            else:
                self.errorString+='\n'+name+':'+'\nXML: '+old+'\nDB: '+new

    def printResult(self):
        if len(self.result):
            print '\nrules are changed %s:\n' % len(self.result)
            for item in self.result.keys():
                print '\n%s: %s' %(item, self.result[item])
        else:
            print 'No system rule changed.'

        if self.errorString!='':
            print self.errorString

if __name__=='__main__':
    myExpect=[{'name': 'eventType', 'value': 'Snort-1325'}, {'name': 'destIpAddr', 'value': '20.1.1.1'}, {'name': 'destIpPort', 'value': '22'}, {'name': 'srcIpPort', 'value': '1111'}, {'name': 'ipProto', 'value': 'TCP'}, {'name': 'ipProto', 'value': 'TCP'}, {'name': 'srcIpAddr', 'value': '20.1.1.1'}]
    myActual=[{'name': 'eventType', 'value': 'Snort-1325'}, {'name': 'ipProto', 'value': '6'}, {'name': 'ipProto', 'value': 'TCP(6)'}, {'name': 'srcIpPort', 'value': '1111'}, {'name': 'destIpPort', 'value': '22'}, {'name': 'destIpPort', 'value': 'SSH(22)'}, {'name': 'destIpAddr', 'value': '20.1.1.1'}, {'name': 'srcIpAddr', 'value': '20.1.1.1'}, {'name': 'eventName', 'value': 'EXPLOIT ssh CRC32 overflow filler'}]


