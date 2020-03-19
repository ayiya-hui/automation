import re
import math

def Add(a, b):
    if '.' in a or '.' in b:
        return float(a)+float(b)
    else:
        return int(a)+int(b)

def Substrict(a, b):
    if '.' in a or '.' in b:
        return float(a)-float(b)
    else:
        return int(a)-int(b)

def Multiply(a, b):
    if '.' in a or '.' in b:
        return float(a)*float(b)
    else:
        return int(a)*int(b)

def Divide(a, b):
    if '.' in a or '.' in b:
        return float(a)/float(b)
    else:
        return int(a)/int(b)

cal_dict={'+':Add,
          '-':Substrict,
          '*':Multiply,
          '/':Divide,}

def calculateTwo(cal, a, b):
    return cal_dict[cal](a, b)

def Equal(a, b):
    if a==b:
        return True
    else:
        return False

def NotEqual(a, b):
    if a!=b:
        return True
    else:
        return False

def Large(a, b):
    if a>b:
        return True
    else:
        return False

def LargeEqual(a, b):
    if a>=b:
        return True
    else:
        return False

def Small(a, b):
    if a<b:
        return True
    else:
        return False

def SmallEqual(a, b):
    if a<=b:
        return True
    else:
        return False

def IN(a, b):
    if a in b:
        return True
    else:
        return False

def NotIn(a, b):
    if a not in b:
        return True
    else:
        return False

def Contain(a, b):
    if b in a:
        return True
    else:
        return False

def NotContain(a, b):
    if b not in a:
        return True
    else:
        return False

tokenOper={'=':Equal,
           '!=':NotEqual,
           '>':Large,
           '>=':LargeEqual,
           '<':Small,
           '<=':SmallEqual,
           'IN':IN,
           'NOT IN':NotIn,
           'CONTAINT':Contain,
           'NOT CONTAIN':NotContain}

def CompareTwo(oper, a, b):
    return tokenOper[oper](a, b)

def splitByNum(total, split):
    num=total/split
    if total%split>0:
        num+=1

    return num

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

def isWrap(value, wrap):
    SPEC={'testcases':['eventParsingCase', 'incidentCase'],
          'events':'incidentEvent',
          'actions':'notificationActions',
          }
    if getPlural(value)==wrap:
        return True
    else:
        if wrap in SPEC.keys() and value in SPEC[wrap]:
            return True
        else:
            return False

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
