import re
import Models.incidentRule as incidentRule

device_exp='Addr IN \(Group@PH_SYS_DEVICE_(?P<deviceGroup>\S+)\)'
eventType_exps={'single':'eventType = "(?P<eventType>\S+)"',
                'group':'eventType IN (?:\()?(?P<eventType>\S+)(?:\))?',
                'notgroup':'eventType NOT IN (?:\()?(?P<eventType>\S+)(?:\))?'}

def readRule(rule):
    singleConstriants=[]
    groupConstriants=[]
    if hasattr(rule, 'eventFilters'):
        eventFilters=getattr(rule, 'eventFilters')
        for item in eventFilters:
            groupCon=getattr(item, 'groupConstraint')
            if not groupCon in groupConstriants:
                groupConstriants.append(groupCon)
            singleCon=getattr(item, 'singleConstraint')
            if not singleCon in singleConstriants:
                singleConstriants.append(singleCon)
    finalGroup=groupConstriants[0]
    if len(groupConstriants)>1:
        print 'more than one groupConstriant'
    deviceCreate=False
    eventTypes=[]
    i=1
    for dat in singleConstriants:
        if not deviceCreate:
            deviceCreate, grpType=isDeviceNeedtoCreated(dat)
        eventType, style=getEventType(dat)
        if eventType and style:
            eType=incidentRule.eventMsgType()
            eType.setType(style, eventType, i)
            i+=1
            eventTypes.append(eType)
    myRuleObj=incidentRule.rule()
    print finalGroup
    rawCount=finalGroup.split('>')[-1]
    if '= ' in rawCount:
        rawCount=rawCount.replace('= ', '')
        myRuleObj.count=int(rawCount)
    else:
        myRuleObj.count=int(rawCount)+1
    print myRuleObj.count
    print 'eventTypes:',eventTypes
    myRuleObj.eventTypes=eventTypes
    if deviceCreate:
        myRuleObj.setCreateDevice(grpType)

    return myRuleObj

def isDeviceNeedtoCreated(constr):
    need=False
    deviceGrpType=''
    myExp=re.compile(device_exp)
    ret=myExp.search(constr)
    if ret:
        need=True
        deviceGrpType=ret.group('deviceGroup')

    return need, deviceGrpType

def getEventType(constr):
    print constr
    eventType=''
    style=''
    for key in eventType_exps.keys():
        myExp=re.compile(eventType_exps[key])
        ret=myExp.search(constr)
        if ret:
            eventType=ret.group('eventType').replace('"','').replace(')','')
            style=key
            break

    return eventType, style

