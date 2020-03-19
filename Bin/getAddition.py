import getAdd

def getData(appServer):
    ruleDbParam,reptDbParam=getAdd.getAddFromDB(appServer)
    print 'Total rules: %s' % len(ruleDbParam)
    print 'Total reports: %s' % len(reptDbParam)

def getAddition(oldAppServer, newAppServer):
    oldEventDbParams,oldRuleDbParams,oldReptDbParams=getAdd.getAddFromDB(oldAppServer, event=True, rule=True, report=True)
    newEventDbParams,newRuleDbParams,newReptDbParams=getAdd.getAddFromDB(newAppServer, event=True, rule=True, report=True)
    output('eventType', oldEventDbParams, newEventDbParams)
    output('rule', oldRuleDbParams, newRuleDbParams)
    output('report', oldReptDbParams, newReptDbParams)

def output(type, oldDbParams, newDbParams):
    delData=[]
    newData=[]
    myVal=''
    print 'Old Total %ss: %s\n' % (type, len(oldDbParams))
    print 'New Total %ss: %s\n' % (type, len(newDbParams))
    for item in newDbParams.keys():
        if item not in oldDbParams.keys():
            newData.append(newDbParams[item])

    for item in oldDbParams.keys():
        if item not in newDbParams.keys():
            delData.append(oldDbParams[item])
    if len(newData)>0:
        print 'There are %s new %ss added:' % (len(newData),type)
        for item in newData:
            if type=='eventType':
                myVal='Display'
            else:
                myVal='Active'
            print '%s name: %s, %s: %s' % (type,item['Name'], myVal, item[myVal])
    else:
        print "There are NO new %s added." % type

    if len(delData)>0:
        print 'There are %s old %ss deleted:' % (len(delData),type)
        for rule in delData:
            print '%s name: %s, %s: %s' % (type,rule['Name'],myVal,rule[myVal])
    else:
        print "There are NO old %ss deleted." % type

if __name__=='__main__':
    import sys
    getAddition(sys.argv[1], sys.argv[2])

