import re
import math

def multiReplace(text, repDict):
    rx=re.compile('|'.join(map(re.escape, repDict)))
    def one_xlat(match):
        return repDict[match.group(0)]
    return rx.sub(one_xlat, text)

def getPlural(value):
    if value[-1]=='y':
        value=value[0:-1]+'ies'
    else:
        value=value+'s'

    return value

def compareValues(oper, value1, value2):
    if oper=='>':
        if value1>value2:
            ret=True
        else:
            ret=False
    elif oper=='>=':
        if value1>=value2:
            ret=True
        else:
            ret=False
    elif oper=='<':
        if value1<value2:
            ret=True
        else:
            ret=False
    elif oper=='<=':
        if value1<=value2:
            ret=True
        else:
            ret=False
    elif oper=='==':
        if value1==value2:
            ret=True
        else:
            ret=False

    return ret

def percentile(list, percent, key=lambda x:x):
    if not len(list):
        return 0.00
    list.sort()
    k=(len(list)-1)*percent*0.01
    f=math.floor(k)
    c=math.ceil(k)
    if f==c:
        return key(list[int(k)])
    d0=key(list[int(f)])*(k-f)
    d1=key(list[int(c)])*(c-k)

    return d0+d1

def floatStrip(value):
    if value==int(value):
        return str(int(value))
    else:
        return str(value)

def roundNumber(value, pos):
    h="%."+str(pos)+"f"
    newValue=h % round(float(value), pos)

    return newValue


if __name__=='__main__':
    mylist=['0.02','0.03','0.04']
    print mylist
    myPer=95
    myPercentile=percentile(mylist, myPer)
    print myPercentile
