import re
import ExpressionDataClass
import classUtility


EXPRESSIONS=['DayOfWeek', 'HourOfDay', 'DeviceToCMDBAttr', 'LAST', 'FIRST', 'AVG', 'SUM', 'MIN', 'MAX', 'Pctile95', 'PctChange']
KEY_EXPS='%s\(([^\)]+)\)'
CMDB='%s\((?P<paramName>\S+):(?P<paramValue>\S+)\)'
DEVICE_GRP='deviceGroup'
PROPERTIES=['country', 'state', 'city', 'building', 'floor']
CONSTR='%s IN (%s)'

def getConstrOperators(expData, appServer):
    #singleConstr
    params=expData.singleConstr.split('AND')
    constrFilters=[]
    newConstrList=[]
    for par in params:
        matched, key=keyMatch(par)
        if matched:
            oper=ExpressionDataClass.constrOperator()
            oper.exp=key
            parList=par.strip().split(' ')
            holder, oper.oper, oper.value=par.strip().split(' ', 2)

            attrName, newValue=replaceExpression(key, holder)
            oper.attr=attrName
            constrFilters.append(oper)

    newConstr=getSpecailConstr(key, params, appServer)
    if not newConstr:
        newConstr='*'

    expData.singleConstr=newConstr
    #group by
    groupbyFilter=ExpressionDataClass.normalOperator()
    matched, groupbyFilter.exp=keyMatch(expData.groupBy)
    newGroupby=getSimpleValue(expData.groupBy)
    groupbyFilter.regular=newGroupby
    expData.groupBy=newGroupby
    if groupbyFilter.exp in ['DayOfWeek', 'HourOfDay']:
        groupbyFilter.exp=groupbyFilter.exp+'##'+constrFilters[0].attr

    #display
    displayFilter=ExpressionDataClass.normalOperator()
    oldList=expData.attr.strip().split(',')
    newDisplay=getSimpleValue(expData.attr)
    expData.attr=newDisplay
    oldKeys=[]
    for key in oldList:
        if key not in newDisplay.split(','):
            oldKeys.append(key)
    rawKey=','.join(oldKeys)
    matched, displayFilter.exp=keyMatch(rawKey)
    newKeys=[]
    for key1 in newDisplay.split(','):
        if key1 in oldList:
            newKeys.append(key1)
    displayFilter.regular=','.join(newKeys)

    if displayFilter.exp in ['LAST', 'FIRST', 'MIN', 'MAX', 'Pctile95', 'PctChange', 'AVG', 'SUM']:
        oper=ExpressionDataClass.constrOperator()
        oper.exp=displayFilter.exp
        constrFilters.append(oper)
        expData.groupBy=''
        for old in oldList:
            if old not in newDisplay.split(','):
                displayFilter.exp=old
        myAttr, myVal=replaceExpression(oper.exp, old)
        groupbyFilter.value=myAttr
        for item in ['LAST', 'FIRST', 'PctChange']:
            if item in displayFilter.exp:
                expData.attr+=',phRecvTime'

    if displayFilter.exp in ['DayOfWeek', 'HourOfDay']:
        displayFilter.exp=displayFilter.exp+'##'+constrFilters[0].attr

    if displayFilter.exp=='None':
        regulars=displayFilter.regular.split(',')
        for key in regulars:
            if 'COUNT' in key:
                displayFilter.regular=key
            else:
                displayFilter.exp=key

    return expData, constrFilters, groupbyFilter, displayFilter

def getSpecailConstr(key, params, appServer):
    constr=''
    if key=='DeviceToCMDBAttr':
        body, value=params[0].split('=')
        value=value.replace('"','')
        pattern=re.compile(CMDB % key)
        ret=pattern.search(body)
        paramName=ret.group('paramName')
        paramValue=ret.group('paramValue')
        if paramValue==DEVICE_GRP:
            import entityValueHandler
            myEntity=entityValueHandler.entityValueHandler(appServer)
            myEntity.getEntityValue(value.strip())
            if hasattr(myEntity, 'data'):
                ips=','.join(myEntity.data)
                constr=CONSTR % (paramName, ips)
            else:
                print 'no data returned. exit'
                exit()
        elif paramValue in PROPERTIES:
            import devicePropertyHandler
            myProperty=devicePropertyHandler.devicePropertyHandler(appServer)
            ips=myProperty.getIpbyProperty(paramValue, value)
            constr=CONSTR % (paramName, ','.join(ips))
        else:
            print 'The param %s is not supported. exit.'
            exit()
    else:
        constr=' AND '.join(params)

    return constr

def getSimpleValue(oldValue):
    valueList=oldValue.strip().split(',')
    newValues=[]
    for value in valueList:
        matched, key=keyMatch(value)
        if not matched:
            newValue=value
        else:
            attrName, newValue=replaceExpression(key, value)
        if newValue:
            newValues.append(newValue)

    return ','.join(newValues)

def keyMatch(value):
        match=False
        for key in EXPRESSIONS:
            if key in value:
                match=True
                return match, key
            else:
                match=False

        return match, 'None'

def replaceExpression(key, value):
        exp=KEY_EXPS % key
        pattern=re.compile(exp)
        ret=pattern.search(value)
        attrName=ret.groups()[0]
        if ':' in attrName:
            attrName=''
        newValue=re.sub(pattern, attrName, value)

        return attrName, newValue


if __name__=='__main__':
    appServer='192.168.20.116'
    expData=ExpressionDataClass.ExpressionData()
    expData.singleConstr='HourOfDay(reptDevIpAddr) < 22'
    expData.groupBy='HourOfDay(phRecvTime)'
    expData.attr='HourOfDay(phRecvTime),COUNT(*)'
    newExpData, constrFilter, groupbyFilter, displayFilter=getConstrOperators(expData, appServer)
    print 'singleConstr: %s' % newExpData.singleConstr
    print 'groupby: %s' % newExpData.groupBy
    print 'attrList: %s' % newExpData.attr
    for constr in constrFilter:
        print 'constrFilter: exp: %s, attr: %s, oper: %s, value: %s' %(constr.exp, constr.attr, constr.oper, constr.value)
    print 'groupbyFilter: exp: %s, regular: %s, value: %s' % (groupbyFilter.exp, groupbyFilter.regular, groupbyFilter.value)
    print 'displayFilter: exp: %s, regular: %s' % (displayFilter.exp, displayFilter.regular)

