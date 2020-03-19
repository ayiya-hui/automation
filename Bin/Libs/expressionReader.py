import re, types
import Models.ClassLocator as classLocator
from restApiDataHandler import restApiDataHandler
import Util.classUtility as classUtility

replace_exp={'single':'(?P<oper>(NOT )?IN)\s+\((?P<name>[^\)]+)\)',
             'group':'(?P<oper>(AVG|COUNT\s?|SUM|PH_FUNC_DIFF_STAT_AVG_1))\s?\((DISTINCT)?\s?(?P<name>[^\)]+)\)',}

simple_exp={'single':'(?P<name>\S+)\s?(?P<operator>(((NOT )?(CONTA)?IN)|[!=><]{1,2}))\s?(?P<value>[\S\d\.,\s]+)',
            'group':'(?P<func>(AVG|COUNT|SUM))\s*(?P<name>\S+)\s?(?P<operator>[><=]{1,2})\s?(?P<value>[\d\.]+)',
            'accelops':'(?P<accelops_name>\S+)\s(?P<func>\S+)\s(?P<name>\S+),\s?(?P<accelops_value>[\d\.]+)\s?(?P<operator>[><=]{1,2})\s?(?P<value>[\d\.]+)',
            'sum_divide':'(?P<func1>(SUM))\s(?P<name1>[^/]+)(?P<param_operator>(/))(?P<func2>(SUM))\s(?P<name2>\S+)\s(?P<operator>[><=]{1,2})\s?(?P<value>[\d\.]+)',
            }
null_or_not={' IS NOT NULL':'!=', ' IS NULL':'='}

values_key=['name', 'operator', 'value', 'func', 'accelops_name', 'accelops_value', 'name1', 'name2', 'func1', 'func2', 'param_operator']

def expressionReader(param, server, option='single'):
    """This method takes a math expression and create a logic way to handle it.
    Mainly use for incident troubleshooting."""
    param=param.replace('\n','')
    if option not in replace_exp.keys():
        print 'option %s is not supported.' % option
        exit()
    myConstriant=None
    reobj=re.compile(replace_exp[option])
    if 'PH_FUNC_DIFF_STAT_AVG_1' in param:
        preRes=reobj.sub(r"\g<oper> \g<name>", param)
    else:
        preRes=param
    result=reobj.sub(r"\g<oper> \g<name>", preRes)
    if re.search(r"\(", result):
        myConstriant=__complexReader(result, server, option)
    else:
        myConstriant=__simpleReader(result.replace('"', ''), server, option)

    return myConstriant

def __complexReader(complex, server, option):
    startPos=[]
    endPos=[]
    for t in re.finditer(r"\(", complex):
        startPos.append(t.start())
    for t in re.finditer(r"\)", complex):
        endPos.append(t.end())
    myComplex=classLocator.getClassObj('complexConstriant', module='constriant')
    if startPos:
        simple=complex[:startPos[0]]+' '+complex[(endPos[-1]+1):]
        if simple:
            mySimple=__simpleReader(simple.replace('"', ''), server, option)
            myComplex.subConstriants.extend(mySimple.subConstriants)
            myComplex.operator=mySimple.operator

        if (len(startPos)==1 and len(endPos)==1) or (startPos[0]+1==startPos[1] and endPos[-2]+1==endPos[-1]):
            sub_complex=complex[(startPos[0]+1):(endPos[-1]-1)]
            subComplex=__complexReader(sub_complex, server, option)
            myComplex.subConstriants.append(subComplex)
        elif startPos[1]>endPos[0]:
            sub_list=[]
            oper=complex[endPos[0]+1:startPos[1]-1]
            for i in range(len(startPos)):
                sub_list.append(complex[startPos[i]+1:endPos[i]-1])
            myComplex.operator=oper
            for item in sub_list:
                subComplex=__complexReader(item, server, option)
                myComplex.subConstriants.append(subComplex)

    else:
        mySimple=__simpleReader(complex.replace('"', ''), server, option)
        myComplex.subConstriants.extend(mySimple.subConstriants)
        myComplex.operator=mySimple.operator

    #remove dubious complex contriant which is actually simple contriant
    if classUtility.getType(myComplex)=='complexConstriant':
        if myComplex.operator=='None' and len(myComplex.subConstriants)==1 and classUtility.getType(myComplex.subConstriants[0])!='complexConstriant':
            myNew=myComplex.subConstriants[0]
            myComplex=myNew

    return myComplex

def __simpleReader(simple, server, option):
    myComplex=classLocator.getClassObj('complexConstriant', module='constriant')
    myRest=restApiDataHandler(server)
    oper=''
    if ' AND ' in simple:
        oper='AND'
    elif ' OR ' in simple:
        oper='OR'
    else:
        oper='None'
    myComplex.operator=oper
    simpleList=simple.split(oper+' ')
    for item in simpleList:
        if item.strip():
            mySimple=None
            key=option
            if option=='single':
                mySimple=classLocator.getClassObj('simpleConstriant', module='constriant')
            else:
                if item.startswith('PH_FUNC_DIFF_STAT_AVG_1'):
                    mySimple=classLocator.getClassObj('accelopsConstriant', module='constriant')
                    key='accelops'
                elif item.startswith('SUM') and '/' in item and item.split('/')[-1].startswith('SUM'):
                    mySimple=classLocator.getClassObj('complexGroupConstriant', module='constriant')
                    key='sum_divide'
                else:
                    mySimple=classLocator.getClassObj('groupConstriant', module='constriant')
            mySimple.desc=item
            nullKey=isNullOrNot(item.strip())
            if nullKey:
                mySimple.name=item.split(nullKey)[0].strip()
                mySimple.operator=null_or_not[nullKey]
                mySimple.value='NULL'
            else:
                reobj=re.compile(simple_exp[key])
                ret=reobj.search(item.strip())
                if ret:
                    for item in values_key:
                        if item in ret.groupdict().keys():
                            setattr(mySimple, item, ret.group(item))
                        if item=='value' and type(getattr(mySimple, 'value'))!=types.NoneType:
                            if mySimple.operator in ['IN', 'NOT IN']:
                                valueList=mySimple.value.split(',')
                                finalList=[]
                                if type(valueList)!=types.NoneType:
                                    for item in valueList:
                                        if 'Group@' in item:
                                            key=item.split('Group@')[-1].strip()
                                            data=myRest.getData(key, module='namedValue')
                                            finalList.extend(data[key].namedValues)
                                        else:
                                            finalList.append(item.strip())
                                    mySimple.value=finalList
            myComplex.subConstriants.append(mySimple)

    return myComplex

def isNullOrNot(param):
    ret=False
    for key in null_or_not.keys():
        if key in param.strip():
            ret=key

    return ret

if __name__=='__main__':
    host='192.168.20.116'
    param='COUNT(*) >= 2'
    expressionReader(param, host, option='group')
