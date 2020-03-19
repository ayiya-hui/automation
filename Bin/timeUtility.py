import datetime
import time

DAY=["Day", "Days", "Daily","day", "days"]
HOUR=["Hour", "Hours", "Hourly", "hour", "hours"]
MINUTE=["Minute", "Minutes", "minute", "minutes"]
MONTH={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

def makeUptime(upMinute=30*24*60):
    timeDelta=datetime.timedelta(0,0,0,0,upMinute)
    timeNow=datetime.datetime.now()-timeDelta
    uTime=str(int(time.mktime(timeNow.timetuple())))

    return uTime

def getTimeDelta(unit, value):
    if unit in DAY:
        delta=datetime.timedelta(int(value))
    elif unit in HOUR:
        delta=datetime.timedelta(0,0,0,0,0,int(value))
    elif unit in MINUTE:
        delta=datetime.timedelta(0,0,0,0,int(value))
    else:
        print 'TIme Unit %s is not supported. Exit' % unit
        exit()

    return delta

def getPastTime(startTime, unit, value):
    delta=getTimeDelta(unit, value)
    pastTime=startTime-delta
    pastUtime=int(time.mktime(pastTime.timetuple()))

    return pastTime, pastUtime

def getTimeNow(second=False):
    now=datetime.datetime.now()
    if second:
        newNow=datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,0,0)
    else:
        newNow=now
    uNow=int(time.mktime(newNow.timetuple()))

    return newNow, uNow

def getFutureTime(days):
    timeDelta=datetime.timedelta(days)
    futureTime=datetime.datetime.now()+timeDelta

    return int(time.mktime(futureTime.timetuple()))

def getUTimeFromString(string):
    weekday,month,day,myTime,zone,year=string.split(' ')
    hour,minute,second=myTime.split(':')
    newTime=datetime.datetime(int(year),MONTH[month],int(day),int(hour),int(minute),int(second),0)

    return int(time.mktime(newTime.timetuple()))

def MakeTime(startTime, endTime):
    timeParam={}
    duration=''
    startParam=startTime.split(" ")
    if startParam[1] in DAY:
        duration=startParam[0]+'d'
        sDelta=datetime.timedelta(int(startParam[0]))
    elif startParam[1] in HOUR:
        duration=startParam[0]+'h'
        sDelta=datetime.timedelta(0,0,0,0,0,int(startParam[0]))
    elif startParam[1] in MINUTE:
        duration=startParam[0]+'m'
        sDelta=datetime.timedelta(0,0,0,0,int(startParam[0]))
    else:
        print "Time Unit is not correct. Exit."
        exit()
    endParam=startTime.split(" ")
    if endParam[1] in DAY:
        eDelta=datetime.timedelta(int(endParam[0]))
    elif endParam[1] in HOUR:
        eDelta=datetime.timedelta(0,0,0,0,0,int(endParam[0]))
    elif endParam[1] in MINUTE:
        eDelta=datetime.timedelta(0,0,0,0,int(endParam[0]))
    else:
        print "Time Unit is not correct. Exit."
        exit()

    eTimeNow=datetime.datetime.now()-eDelta
    sTimeNow=eTimeNow-sDelta

    sTimeParam={}
    sTimeParam['cTime']=sTimeNow.isoformat(" ").split(".")[0]
    sTimeParam['uTime']=str(int(time.mktime(sTimeNow.timetuple())))

    eTimeParam={}
    eTimeParam['cTime']=eTimeNow.isoformat(" ").split(".")[0]
    eTimeParam['uTime']=str(int(time.mktime(eTimeNow.timetuple())))

    timeParam['startTime']=sTimeParam
    timeParam['endTime']=eTimeParam
    timeParam['duration']=duration

    return timeParam

if __name__=='__main__':
    myStr='Sat May 28 00:23:41 UTC 2011'
    myTime=getUTimeFromString(myStr)
    print myStr
    print myTime

