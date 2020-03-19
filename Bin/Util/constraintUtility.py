import re
import classUtility
import generalUtility

single_constriant_exp='(?P<name>\S+)\s+(?P<oper>(([><=]{1,2})|(NOT )?(IN|CONTAIN)))\s(?P<value>[\s\S]+)'
replace_dict={'(':'', ')':''}
special_words={' IS NOT NULL':'!=#NULL', ' IS NULL':'=#NULL'}
divide_sum='SUM\((?P<name1>\S+)\)/SUM\((?P<name2>\S+)\)\s?(?P<oper>[><=]{1,2})\s?(?P<value>[0-9\.]+)'
group_constriant_exp_head='^COUNT\s?\((DISTINCT\s?)?(?P<name>\S+)\)\s?(?P<oper>[><=]{1,2})\s?(?P<value>\S+)(\s+AND\s+(?P<extra>[\s\S]+))?'
group_constriant_exp_tail='(?P<extra>[\s\S]+)\s+AND\s+COUNT\s?\((?P<name>\S+)\)\s?(?P<oper>[><=]{1,2})\s?(?P<value>\S+)'
group_constriant_cond='[\(]{0,2}(?P<typeName>[A-Z]+)\((?P<name>[a-zA-Z]+)\)\s?(?P<oper>[><=]{1,2})\s?(?P<value>[0-9\.]+)'
group_specail_func={'PH':''}
OPER_KEY={'=':'Equal','>=':'LargeEqual', '<=':'SmallEqual', '>':'Large', '<':'Small'}

def processConstraint(param, groupBy=False, groupConstr=False):
    """
    This utility will pick up the SingleConstriant, GroupBy and GroupConstraint data, then break them down to fill a dict.
    """
    map={}
    map['SingleConstriant']={}
    paramList=param.split(' AND ')
    pattern=re.compile(single_constriant_exp)
    for item in paramList:
        key=isSpecial(item)
        if key:
            name=item.split(key)[0].strip()
            content=special_words[key]
        else:
            ret=pattern.search(item.strip())
            if ret:
                name=ret.group('name')
                value=ret.group('value')
                oper=ret.group('oper')
                if oper!='=':
                    value=generalUtility.multiReplace(value, replace_dict)
                value=value.replace('"', '').replace(' ', '')
                if ',' in value:
                    value=value.replace(',', '&')
                content=oper+'#'+value
        if name in map['SingleConstriant'].keys():
            newList=map['SingleConstriant'][name]
            newList.append(content)
            map['SingleConstriant'][name]=newList
        else:
            map['SingleConstriant'][name]=[content]
    if groupBy:
        groupbys=groupBy.split(',')
        map['GroupBy']=groupbys
    if groupConstr:
        groupConstr=groupConstr.replace('\n', '')
        map['GroupConstriant']={}
        if '/SUM' in groupConstr:
            pattern=re.compile(divide_sum)
            ret=pattern.search(groupConstr.strip())
            if ret:
                name1=ret.group('name1')
                name2=ret.group('name2')
                oper=ret.group('oper')
                value=ret.group('value')
                content=name1+'&'+name2+'#'+oper+'#'+value
                map['GroupConstriant']['DIV_SUM']=content
        else:
            pattern=None
            if groupConstr.startswith('COUNT'):
                pattern=re.compile(group_constriant_exp_head)
            else:
                pattern=re.compile(group_constriant_exp_tail)
            ret=pattern.search(groupConstr.strip())
            if ret:
                extra=None
                if ret.groupdict().has_key('extra'):
                    extra=ret.group('extra')
                name=ret.group('name')
                value=ret.group('value')
                oper=ret.group('oper')
                map['GroupConstriant']['COUNT']=name+'#'+oper+'#'+value
                if extra:
                    conMap=getExtraCondition(extra)
                    map['GroupConstriant']['COND']=conMap

    return map

def isSpecial(param):
    ret=False
    for key in special_words.keys():
        if key in param.strip():
            ret=key

    return ret


def getExtraCondition(extra):
    pattern=re.compile(group_constriant_cond)
    condMap={}
    condList=None
    if extra.startswith('((') or (' OR ' in extra and ' AND ' in extra):
        condMap['oper']='OR'
        conds=[]
        myCond=extra.split('OR')
        for subCon in myCond:
            subMap=getCond(pattern, subCon.split(' AND '), 'AND')
            conds.append(subMap)
        condMap['param']=conds
    else:
        if ' OR ' in extra:
            condMap=getCond(pattern, extra.split(' OR '), 'OR')
        elif ' AND ' in extra:
            condMap=getCond(pattern, extra.split(' AND '), 'AND')
        else:
            condMap=getCond(pattern, [extra], 'NONE')

    return condMap

def getCond(pattern, conList, oper):
    condMap={}
    condMap['oper']=oper
    param=[]
    for item in conList:
        ret=pattern.search(item)
        if ret:
            typeName=ret.group('typeName')
            name=ret.group('name')
            oper=ret.group('oper')
            value=ret.group('value')
            content=name+'#'+oper+'#'+value
            bottomMap={}
            bottomMap[typeName]=content
            param.append(bottomMap)
    condMap['param']=param

    return condMap


if __name__=='__main__':
    #param='eventType = "a" AND b NOT IN (Group@c)'
    param='(reptDevIpAddr IN (Group@PH_SYS_DEVICE_NETWORK_IPS) OR (reptDevIpAddr IN (Group@PH_SYS_APP_NETWORK_IPS) AND eventType CONTAIN "Snort-")) AND reptVendor != "Cisco" AND eventType NOT IN (Group@PH_SYS_EVENT_Logon,Group@PH_SYS_EVENT_Reconn) AND eventSeverity >= 8'
    #group='((AVG(nfsReadLatency)>=50 AND (AVG(nfsReadLatency)<=100) OR (AVG(nfsWriteLatency)>=50 AND AVG(nfsWriteLatency)<=100)) AND COUNT(*)>=2'
    #group='(AVG(nfsReadLatency)>=50 OR (AVG(nfsWriteLatency)>=50) AND COUNT(*)>=2'
    #group='AVG(a)>1 OR AVG(b)>1 AND COUNT(*)>=2'
    #group='AVG(a)>1 AND AVG(b)>1 AND AVG(c)>1 AND COUNT(*)>=2'
    group='PH_FUNC_DIFF_STAT_AVG_1(SUM(totFlows), 2.0) >= 0 AND PH_FUNC_DIFF_STAT_AVG_1(SUM(totBytes), 2.0) >= 0 AND SUM(totFlows) >= 2000'
    groupby='hostIpAddr,hostName'
    data=processConstraint(param, groupBy=groupby, groupConstr=group)
    print data['SingleConstriant']
    print data['GroupConstriant']





