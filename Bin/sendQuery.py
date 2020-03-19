import queryHandler, sys, re

EXP='%s\((\S+)\)'
CONSTR='%s AND %s = "%s"'

def removeExp(expType, value):
    exp=EXP % expType
    pattern=re.compile(exp)
    ret=pattern.search(value)
    attrName=ret.groups()[0]
    newValue=re.sub(pattern, attrName, value)

    return attrName, newValue

appServer=sys.argv[1]
fileName=sys.argv[2]
myFile=open(fileName)
myLines=myFile.readlines()
myFile.close()
myQuery=queryHandler.queryHandler()
expRet=''
traRet=''
for line in myLines:
    expType, singleConstr, groupby, attr, time, value=line.split(';')
    attrName, attr1=removeExp(expType, attr)
    myQuery.getQuery(appServer, singleConstr, groups=groupby, filter=attr, timeUnit=time, timeValue=value)
    expRet=myQuery.data
    expCount=len(myQuery.data)
    myQuery.getQuery(appServer, singleConstr, groups=groupby, filter=attr1, timeUnit=time, timeValue=value)
    traRet=myQuery.data
    exp1Count=len(myQuery.data)

    print 'Expression Query Count %s' % expCount
    print 'Tradition Query Count %s' % exp1Count
    if expCount == exp1Count:
        print 'Count is same.'
    else:
        print 'Count is NOT same.'
    final={}
    for data in traRet:
        constr=CONSTR % (singleConstr, groupby, data[groupby])
        myQuery.getQuery(appServer, constr, filter=attr1, timeUnit=time, timeValue=value)
        myRetData=myQuery.data
        values=[]
        for data in myRetData:
            values.append(data[attrName])
        values.sort()
        final[data[groupby]]=values[-1]

    correct=[]
    error=[]
    for data in expRet:
        key1, key2=attr.split(',')
        value=final[data[key1]]
        map={}
        map[key1]=data[key1]
        map[key2]=data[key2]
        map['tradtion']=value
        if data[key2]==value:
            correct.append(map)
        else:
            error.append(map)

        print 'Total correct: %s' % len(correct)
        print 'Total error: %s' % len(error)
        print 'Error details:'
        for item in error:
            for key in item.keys():
                print '%s: %s' % (key, itme[key])
