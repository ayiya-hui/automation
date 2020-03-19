import Util.classUtility as classUtility
from ConfigConstants.TestConstant import approved_device_params
import Util.generalUtility as generalUtility

ERROR_MSG='Condition: "%s" not met.'
OP_WORDS={'IN':'not in', 'NOT IN':'in'}

def expressionEval(finalMsgs, singleConstr, groupConstr, groupbyConstr, approved):
    """This method will evaluate the expression logic. Mainly for incident
    troubleshooting."""
    #test singleConstr
    singleCheck=True
    singleReason=''
    if singleConstr:
        singleCheck, singleReason=__evalExpression(finalMsgs, singleConstr)
    #test groupConstr
    groupCheck=True
    groupReason=''
    if groupConstr:
        groupCheck, groupReason=__evalExpression(finalMsgs, groupConstr)
    #test groupbyConstr
    groupbyCheck=True
    groupbyReason=''
    if groupbyConstr:
        groupbyCheck, groupbyReason=__evalGroupBy(finalMsgs, groupbyConstr)
    #test approved
    check=True
    reason=''
    if approved.approvedDevicesOnly=='true':
        check, reason=__evalApprove(finalMsgs, approved)
    finalCheck=singleCheck and groupCheck and groupbyCheck and check
    finalErrors=[]
    if singleReason:
        finalErrors.append(singleReason)
    if groupReason:
        finalErrors.append(groupReason)
    if groupbyReason:
        finalErrors.append(groupbyReason)
    if reason:
        finalErrors.append(reason)
    if finalErrors:
        finalStr=';'.join(finalErrors)
    else:
        finalStr='All condtions are met. Issue in the codes.'

    return finalCheck, finalStr

def __evalExpression(msgs, constrobj):
    retMsg=[]
    errors=''
    if constrobj.operator=='None':
        ret, errors=__evalExpression(msgs, constrobj.subConstriants[0])
        retMsg.append(errors)
    else:
        if hasattr(constrobj, 'subConstriants'):
            for constr in constrobj.subConstriants:
                ret=None
                errors=''
                if classUtility.getType(constr)=='complexConstriant':
                    ret, errors=__evalExpression(msgs, constr)
                else:
                    ret, errors=__evalSimpleExpression(msgs, constr)
                if errors:
                    retMsg.append(errors)
        else:
            ret=None
            errors=''
            if classUtility.getType(constrobj)=='complexConstriant':
                ret, errors=__evalExpression(msgs, constrobj)
            else:
                ret, errors=__evalSimpleExpression(msgs, constrobj)
            if errors:
                retMsg.append(errors)

        if constrobj.operator=='AND' and not retMsg:
            ret=True
        else:
            ret=False

        if constrobj.operator=='OR' and len(retMsg)<len(msgs):
            ret=True
        else:
            ret=False

    return ret, ';'.join(retMsg)

def __evalSimpleConstr(msgs, constr):
    errors=''
    check=True
    for msg in msgs:
        if constr.name in msg.attributes.keys():
            ret=generalUtility.CompareTwo(constr.operator, msg.attributes[constr.name], constr.value)
            if not ret:
                errors=ERROR_MSG % constr.desc
                if constr.operator in OP_WORDS.keys():
                    errors+=msg.attributes[constr.name]+' '+OP_WORDS[constr.operator]+' device group.'
                else:
                    errors+='Actual valule: '+msg.attributes[constr.name]
                check=False
        else:
            errors=ERROR_MSG % constr.desc
            errors+='No parameter '+constr.name+' in actual message.'
            check=False

    return check, errors

def __evalGroupConstr(msgs, constr):
    errors=''
    check=True
    finalVal=__getFuncValue(msgs, constr.name, constr.func)
    ret=generalUtility.CompareTwo(constr.operator, finalVal, constr.value)
    if not ret:
        errors=ERROR_MSG % constr.desc
        errors+='Actual value: '+finalVal
    return check, errors

def __evalComplexGroupConstr(msgs, constr):
    errors=''
    check=True
    value1=__getFuncValue(msgs, constr.name1, constr.func1)
    value2=__getFuncValue(msgs, constr.name2, constr.func2)
    value=generalUtility.calculateTwo(constr.param_operator, value1, value2)
    ret=generalUtility.CompareTwo(constr.operator, finalVal, constr.value)
    if not ret:
        errors=ERROR_MSG % (constr.desc, msg.attributes[constr.name])
    return check, errors

def __evalAccelopsConstr(msgs, constr):
    return False, ''

token_dict={'simpleConstriant': __evalSimpleConstr,
            'groupConstriant': __evalGroupConstr,
            'complexGroupConstriant': __evalComplexGroupConstr,
            'accelopsConstriant': __evalAccelopsConstr,}

def __evalSimpleExpression(msgs, constr):
    print constr, msgs
    return token_dict[classUtility.getType(constr)](msgs, constr)

def __getAVG(msgs, name):
    value=0
    for msg in msgs:
        if name in msg.attributes:
            if '.' in msg.attributes[name]:
                value+=float(msg.attributes[name])
            else:
                value+=int(msg.attributes[name])
            final=value/len(msgs)
        else:
            final='No %s in params' % name

def __getSUM(msgs, name):
    value=0
    for msg in msgs:
        if '.' in msg.attributes[name]:
            value+=float(msg.attributes[name])
        else:
            value+=int(msg.attributes[name])

    return uvalue

def __getCount(msgs):
    return len(msgs)

def __getDistinctCount(msgs, name):
    values=[]
    for msg in msgs:
        if msg.attributes[name] not in values:
            values.append(msg.attributes[name])

    return len(values)

func_dict={'AVG':__getAVG,
           'SUM':__getSUM,
           'COUNT':__getCount,
           'DistinctCount':__getDistinctCount}

def __getFuncValue(msgs, name, func):
    if func=='COUNT' and name!='*':
        func='DistinctCount'
    if func=='COUNT':
        return unicode(func_dict[func](msgs))
    else:
        return unicode(func_dict[func](msgs, name))

def __evalGroupBy(msgs, groupbyConstr):
    check=True
    errors=[]
    miss=[]
    for msg in msgs:
        for key in groupbyConstr:
            if key not in msg.attributes.keys():
                if key not in miss:
                    miss.append(key)
                    errors.append('GroupBy: %s not in attributes' % key)
    if len(errors):
        check=False

    return check, ';'.join(errors)

def __evalApproved(msgs, approve):
    reason=''
    check=True
    approvedIps=[]
    for sub in approved.approvedDevices:
        approvedIps.append(sub.accessIp)
    keyCheck=[]
    for msg in msgs:
        devIps={}
        keyCheck=[]
        for key in approved_device_params:
            devIps[key]=msg.attributes[key]
        for ipName in devIps.keys():
            if devIps[ipName] in approvedIps:
                keyCheck.append([ipName+'('+devIps[ipName]+')'])
    if not keyCheck:
        reason='Device approve set True, this device is not in the list.'
        check=False

    return check, reason
